!
! First, compute r*Psi4 using the raw Psi4 data corrected to remove gauge effects 
! using the procedure described in PRD 80, 124045 (2009).
! Then calculate r h_+ and r h_x by twice time integration using FFI.
! (See  arXiv:1006.1632)
! Finally, calculate the engergy, angular momentum and linear monentum radiated by the GW.
! 
   implicit none
   real*8, allocatable, dimension(:) :: temp, tret, outarray, rpsi422r,rpsi422i
   real*8, allocatable, dimension(:,:) :: rhp_plus_i_hc
   real*8, allocatable, dimension(:,:) :: rhphc, rhphcdot
   real*8, allocatable, dimension(:,:,:) :: rhplm,rhclm,rhpdlm,rhcdlm
   real*8 :: t0,tend,dt,dw,w_upper_cut, w_lower_cut,int_fact1,int_fact2,w,lambda,gw_lower_cut
   real*8 :: t_start, t_end, t, Madm, R_areal, rstar, tsch, dtc0,dtc1
   real*8 :: tret_start,tret_end, tret_i,temp1, E_GW, J_GW, vx_GW, vy_GW, Px_GW,Py_GW
   real*8 :: guptt, guptr, guprr,dto32pi,omega22
   real*8 :: cplm,c0lm,cmlm,Eplmr,Eplmi,E0lmr,E0lmi,Emlmr,Emlmi,Eplmr1,Eplmi1
   real*8 :: E0lmr1,E0lmi1,Emlmr1,Emlmi1, phase,dphase
   real*8 :: dplm,d0lm,Fplm,F0lm,Fplm1,F0lm1, Pz_GW, vz_GW
   integer :: i,n,num_column,ios,num_modes,j,k,nn, l_gw,m_gw, istart,lmax,ll,mm
   integer, dimension(:), allocatable :: lmode,mmode
   character*50 psi4_filename,hphc_filename
   real*8, parameter :: pi = 3.14159265358979323846d0
   integer, parameter :: inter_order = 4
   real*8, dimension(inter_order) :: xa,ya
   complex*16 :: omega22a, omega22b
!
   ! Note: The parameter w_lower_cut refers to the *orbital* frequency in code unit, 
   !       not the (2,2) mode of GW frequency.
   ! GW strain with t<t_start and t>t_end will be set to 0
   !
   open(1,file='ccc_ffi.input',status='old')
   read(1,*)
   read(1,*) psi4_filename,num_column,w_lower_cut,Madm,t_start,t_end
   close(1)

! The columns of the Psi4 files should be 
!  time, Re(psi4_22), Im(psi4_22), Re(psi4_21), Im(psi4_21), ..., areal radius, <g^tt>, <g^tr>, <g^rr>
! spaced evenly in time with no repeated entries.

   if (mod(num_column,2)==0) then 
      write(*,*) 'Number of column in psi4 files must be an odd number!'
      stop
   end if

   if (num_column .gt. 198) then 
      write(*,*) 'Too many columns! The number of l-modes will reach l>=10, which is not supported yet.'
      stop
   end if

   num_modes = (num_column-5)/2

   allocate( lmode(num_modes) )
   allocate( mmode(num_modes) )
   i = 2
   lmode(1) = 2
   mmode(1) = 2
   do
      do
          if (mmode(i-1) .eq. -lmode(i-1) .or. i .gt. num_modes) exit
          lmode(i) = lmode(i-1)
          mmode(i) = mmode(i-1)-1
          i = i+1
      end do
      if (i .gt. num_modes) exit
      lmode(i) = lmode(i-1)+1
      mmode(i) = lmode(i)
      i = i+1
   end do
   lmax = lmode(num_modes)+1

   allocate( temp(num_column) )
  
   ! It is assumed that the psi4 data are constantly sampled in time and no repeated entries
   open(1,file=psi4_filename,status='old')
   ! Calculate the number of lines in the file and delta t
   read(1,*) t0
   n = 2
   do
       read(1,*,iostat=ios) tend
       if (ios .ne. 0) exit
       n = n+1
   end do
   close(1)
   n = n-1
   dt = (tend-t0)/(n-1)

   if (t_end .ge. tend) t_end = tend-0.5d0*dt
  
   nn = int( log(dble(n))/log(2.d0) - 1.d-10 ) + 3
   nn = 2**nn
   if (nn .lt. n) then 
      write(*,*) "This doesn't make sense. There is a bug somewhere!"
      stop
   end if

   write(*,*) 'Number of lines in file ',psi4_filename,' is ',n
   write(*,*) 'Start time, end times and dt in the file: ',t0,tend,dt

   allocate( rhp_plus_i_hc(num_modes,2*nn))
   allocate( rhphc(num_modes,2*nn))
   allocate( tret(nn) )
   allocate( rpsi422r(nn) )
   allocate( rpsi422i(nn) )
   open(1,file=psi4_filename,status='old')
   read(1,*) temp
   t0 = temp(1)
   R_areal = temp(2*num_modes+2)
   guptt = temp(2*num_modes+3)
   guptr = temp(2*num_modes+4)
   guprr = temp(2*num_modes+5)
   dtc0 = (guptr-sqrt(guptr*guptr - guptt*guprr) )/guptt/(1.d0-2.d0*Madm/R_areal)*dt
   rstar = R_areal + 2.d0*Madm*log( R_areal*0.5/Madm - 1.d0 )
   tsch = t0
   tret(1) = tsch - rstar
   if (t_start .le. t0) tret_start = tret(1)
   if (t_start .ge. t0 .and. t_start .lt. t0+dt) tret_start = tret(1)
   do j=1,num_modes 
      rhp_plus_i_hc(j,1) = temp(2*j)*R_areal
      rhp_plus_i_hc(j,2) = -temp(2*j+1)*R_areal
   end do

   ! t_coord: coordinate time, t_sch: Schwarzschild time, t_retarded: retarded time, 
   ! r_tortoise: tortoise radius 
   open(2,file='times.dat',status='unknown')
   write(2,'("#       t_coord              t_sch            t_retarded          r_tortoise          Re(r Psi4_22)       Im(r Psi4_22)")')
   write(2,'(6ES25.15)') t0,tsch,tret(1),rstar,rhp_plus_i_hc(1,1),-rhp_plus_i_hc(1,2)

   do i=2,n
      read(1,*) temp
      t = t0 + (i-1)*dt
      R_areal = temp(2*num_modes+2)
      guptt = temp(2*num_modes+3)
      guptr = temp(2*num_modes+4)
      guprr = temp(2*num_modes+5)
      dtc1 = (guptr-sqrt(guptr*guptr - guptt*guprr) )/guptt/(1.d0-2.d0*Madm/R_areal)*dt
      tsch = tsch + 0.5d0*(dtc0+dtc1) ! Integrate using the trapzoidal rule
      dtc0 = dtc1
      rstar = R_areal + 2.d0*Madm*log( R_areal*0.5/Madm - 1.d0 )
      tret(i) = tsch - rstar
      if (t_start .ge. t .and. t_start .lt. t+dt) tret_start = tret(i)
      if (t_end .le. t .and. t_end .gt. t-dt) tret_end = tret(i)

      do j=1,num_modes
         rhp_plus_i_hc(j,2*i-1) = temp(2*j)*R_areal
         rhp_plus_i_hc(j,2*i) = -temp(2*j+1)*R_areal
      end do
      write(2,'(6ES25.15)') t,tsch,tret(i),rstar,rhp_plus_i_hc(1,2*i-1),-rhp_plus_i_hc(1,2*i)
   end do
   close(1)
   close(2)

   deallocate(temp)

   do i=n+1,nn
      tret(i) = tret(i-1) + dtc1
      rhp_plus_i_hc(j,2*i-1) = 0.d0
      rhp_plus_i_hc(j,2*i) = 0.d0
   end do

   ! Interpolate to constant dt in retarded time and zero out the data 
   ! for t<t_start and t>t_end.
   ! New r Psi4 data are stored in rhphc array.
   do i=1,nn
      tret_i = tret(1) + dt*(i-1)

      if (tret_i .lt. tret_start .or. tret_i .gt. tret_end) then
         do j=1,num_modes
            rhphc(j,2*i-1) = 0.d0
            rhphc(j,2*i) = 0.d0
         end do
      else
         ! Perform interpolation 
	 do k=1,n-1
            if (tret_i .ge. tret(k) .and. tret_i .lt. tret(k+1)) istart = k
	 end do
         if (tret_i .ge. tret(n)) istart = n
         istart = istart-inter_order/2
         istart = max(istart,0)
         istart = min(istart,n-inter_order)
         do k=1,inter_order 
	    xa(k) = tret(k+istart)
         end do
	 do j=1,num_modes
	    do k=1,inter_order
	       ya(k) = rhp_plus_i_hc(j,2*(k+istart)-1)
	    end do
	    call polint(xa,ya,inter_order,tret_i,rhphc(j,2*i-1),temp1)
	    do k=1,inter_order
               ya(k) = rhp_plus_i_hc(j,2*(k+istart))
            end do
            call polint(xa,ya,inter_order,tret_i,rhphc(j,2*i),temp1)
	 end do
	 rpsi422r(i) = rhphc(1,2*i-1)
	 rpsi422i(i) = -rhphc(1,2*i)
      end if
   end do
   
   deallocate(rhp_plus_i_hc)

   allocate(rhphcdot(num_modes,2*nn))

   dw = 2.d0*pi/(nn*dt)
   w_upper_cut = 0.5d0*n*dw

   ! Now perform forward fft 
   do j=1,num_modes
      call four1(rhphc(j,:),nn,1)
   end do

   ! Now perform time integration in Fourier space
   do i=1,nn/2
      do j=1,num_modes
         !call get_lm(j,l_gw,m_gw)
         l_gw = lmode(j)
         m_gw = mmode(j)
         gw_lower_cut = max(abs(m_gw)*w_lower_cut,w_lower_cut)
         ! First deal with non-negative frequency
         w = dw*(i-1)
         if (w .gt. gw_lower_cut) then 
            int_fact1 = 1.d0/w
	    int_fact2 = -1.d0/(w*w)
         else
            int_fact1 = 1.d0/gw_lower_cut
	    int_fact2 = -1.d0/(gw_lower_cut*gw_lower_cut)
         end if
         !!if(w .gt. w_upper_cut) then 
	 !!  int_fact1 = 1.d0/w_upper_cut
         !!  int_fact2 = -1.d0/w_upper_cut**2
         !!end if
	 rhphcdot(j,2*i-1) = -int_fact1*rhphc(j,2*i)
	 rhphcdot(j,2*i) = int_fact1*rhphc(j,2*i-1)
         rhphc(j,2*i-1) = rhphc(j,2*i-1)*int_fact2
         rhphc(j,2*i) = rhphc(j,2*i)*int_fact2
         ! Now negative frequency 
         w = -dw*i
         if (-w .gt. gw_lower_cut) then
	    int_fact1 = 1.d0/w
            int_fact2 = -1.d0/(w*w)
         else
	    int_fact1 = -1.d0/gw_lower_cut
            int_fact2 = -1.d0/(gw_lower_cut*gw_lower_cut)
         end if
         !!if(-w .gt. w_upper_cut) then 
	 !!  int_fact1 = -1.d0/w_upper_cut
         !!  int_fact2 = -1.d0/w_upper_cut**2
         !!end if
	 rhphcdot(j,2*nn-2*i+1) = -int_fact1*rhphc(j,2*nn-2*i+2)
	 rhphcdot(j,2*nn-2*i+2) = int_fact1*rhphc(j,2*nn-2*i+1)
         rhphc(j,2*nn-2*i+1) = rhphc(j,2*nn-2*i+1)*int_fact2 
         rhphc(j,2*nn-2*i+2) = rhphc(j,2*nn-2*i+2)*int_fact2
      end do
   end do

   ! Now perform backward transform
   do j=1,num_modes
      call four1(rhphcdot(j,:),nn,-1)
      call four1(rhphc(j,:),nn,-1)
   end do
   rhphcdot = rhphcdot/dble(nn)
   rhphc = rhphc/dble(nn)

   ! Output rh_+, rh_x, rhdot_+, rhdot_x, and omega_{22}
   ! omega_{22} are computed in 3 different ways: 
   ! (1) omega_{22} = d (phase22)/dt, where phase22 = arg( h_{+22} + i h_{x22} );
   ! (2) omega_{22} = i Hdotdot_{22}/Hdot_{22}, where H_{22} = h_{+22} - i h_{x22}; 
   ! (3) omega_{22} = i Hdot_{22}/H_{22}.
   allocate( outarray(num_column-4) )
   open(1,file='rhphc.dat',status='unknown')
   open(2,file='rhphcdot.dat',status='unknown')
   open(3,file='omega22.dat',status='unknown')
   do i=1,n
      outarray(1) = tret(1) + dt*(i-1)
      do j=1,num_modes
	 outarray(2*j) = rhphc(j,2*i-1)
	 outarray(2*j+1) = rhphc(j,2*i)
      end do
      write(1,'(999ES25.15)') outarray
      do j=1,num_modes
         outarray(2*j) = rhphcdot(j,2*i-1)
         outarray(2*j+1) = rhphcdot(j,2*i)
      end do
      write(2,'(999ES25.15)') outarray
      if (rpsi422r(i)**2 + rpsi422i(i)**2 .gt. 0.d0) then 
	 phase = atan2(rhphc(1,2*i+2),rhphc(1,2*i+1))
	 if (i==1) then 
	    dphase = phase - atan2(rhphc(1,2),rhphc(1,1))
            if (dphase .lt. -pi) dphase = dphase + 2.d0*pi
            if (dphase .gt. pi) dphase = dphase - 2.d0*pi
         else
	    dphase = phase - atan2(rhphc(1,2*i-2),rhphc(1,2*i-3)) 
            if (dphase .lt. -pi) dphase = dphase + 2.d0*pi
            if (dphase .gt. pi) dphase = dphase - 2.d0*pi
	    dphase = 0.5d0*dphase
         end if
         omega22 = dphase/dt
	 omega22a = dcmplx(0.d0,-1.d0)*dcmplx(rpsi422r(i),-rpsi422i(i)) & 
			/ dcmplx( rhphcdot(1,2*i-1),rhphcdot(1,2*i) )
	 omega22b = dcmplx(0.d0,-1.d0)*dcmplx( rhphcdot(1,2*i-1),rhphcdot(1,2*i) ) & 
			/ dcmplx( rhphc(1,2*i-1),rhphc(1,2*i) )
	 write(3,'(6ES25.15)') tret(1) + dt*(i-1),omega22,dble(omega22a),dimag(omega22a), &
				dble(omega22b),dimag(omega22b)
      end if
   end do
   close(1)
   close(2)
   close(3)
   deallocate(outarray)

   ! Compute E_GW, J_GW, vx_GW and vy_GW
   ! First, rearrange the GW modes into new arrays in order to 
   ! perform the computation more easily.
   allocate( rhpdlm(n,lmax,-lmax:lmax) )
   allocate( rhcdlm(n,lmax,-lmax:lmax) )
   rhpdlm = 0.d0
   rhcdlm = 0.d0
   do i=1,n
      do j=1,num_modes
	 !call get_lm(j,l_gw,m_gw)
         l_gw = lmode(j)
         m_gw = mmode(j)
         rhpdlm(i,l_gw,m_gw) = rhphcdot(j,2*i-1)
         rhcdlm(i,l_gw,m_gw) = rhphcdot(j,2*i)
      end do
   end do
   deallocate(rhphcdot)

   allocate( rhplm(n,lmax,-lmax:lmax) )
   allocate( rhclm(n,lmax,-lmax:lmax) )
   rhplm = 0.d0
   rhclm = 0.d0
   do i=1,n
      do j=1,num_modes
         !call get_lm(j,l_gw,m_gw)
         l_gw = lmode(j)
         m_gw = mmode(j)
         rhplm(i,l_gw,m_gw) = rhphc(j,2*i-1)
         rhclm(i,l_gw,m_gw) = rhphc(j,2*i)
      end do
   end do
   deallocate(rhphc)

   ! Now compute E_GW, J_GW and kick velocity 
   ! using the formulas in YT's GW note. 
   !
   dto32pi = dt/(32.d0*pi)
   E_GW = 0.d0
   J_GW = 0.d0
   Px_GW = 0.d0
   Py_GW = 0.d0
   Pz_GW = 0.d0

   open(1,file='ejv_GW.dat',status='unknown')
   write(1,'("#      t_retarded            E_GW               J_GW               |P_GW|                Px_GW              Py_GW               Pz_GW")')
   do i=1,n-1
      do ll=2,lmax-1
         do mm=-ll,ll
            E_GW = E_GW + dto32pi*(rhpdlm(i,ll,mm)**2 + rhcdlm(i,ll,mm)**2 + &
                              rhpdlm(i+1,ll,mm)**2 + rhcdlm(i+1,ll,mm)**2)
            J_GW = J_GW - dto32pi*mm*( rhpdlm(i,ll,mm)*rhclm(i,ll,mm) &
                              - rhcdlm(i,ll,mm)*rhplm(i,ll,mm) + &
                              rhpdlm(i+1,ll,mm)*rhclm(i+1,ll,mm) &
                              - rhcdlm(i+1,ll,mm)*rhplm(i+1,ll,mm) )
            cplm = -1.d0/dble(ll+1) * sqrt( &
                      (ll+mm+1.d0)*(ll+mm+2.d0)*(ll-1.d0)*(ll+3.d0)/ &
                      (2*ll+1.d0)/(2*ll+3.d0) )
            c0lm = 2.d0/ll/(ll+1)*sqrt( (ll-mm)*(ll+mm+1.d0) )
            cmlm = 1.d0/ll*sqrt( (ll-mm-1.d0)*(ll-mm)*(ll-2.d0)*(ll+2.d0) / &
                                 (2*ll-1.d0)/(2*ll+1.d0) )
   	    dplm = 1.d0/(ll+1) * sqrt( &
			(ll-mm+1.d0)*(ll+mm+1.d0)*(ll-1.d0)*(ll+3.d0)/ &
			((2*ll+1.d0)*(2*ll+3.d0)) )
	    d0lm = 2.d0*mm/(ll*(ll+1))
            Eplmr = rhpdlm(i,ll,mm)*rhpdlm(i,ll+1,mm+1) + rhcdlm(i,ll,mm)*rhcdlm(i,ll+1,mm+1)
            Eplmi = rhpdlm(i,ll,mm)*rhcdlm(i,ll+1,mm+1) - rhpdlm(i,ll+1,mm+1)*rhcdlm(i,ll,mm)
            E0lmr = rhpdlm(i,ll,mm)*rhpdlm(i,ll,mm+1) + rhcdlm(i,ll,mm)*rhcdlm(i,ll,mm+1)
            E0lmi = rhpdlm(i,ll,mm)*rhcdlm(i,ll,mm+1) - rhcdlm(i,ll,mm)*rhpdlm(i,ll,mm+1)
            Emlmr = rhpdlm(i,ll,mm)*rhpdlm(i,ll-1,mm+1) + rhcdlm(i,ll,mm)*rhcdlm(i,ll-1,mm+1)
            Emlmi = rhpdlm(i,ll,mm)*rhcdlm(i,ll-1,mm+1) - rhcdlm(i,ll,mm)*rhpdlm(i,ll-1,mm+1)
            Eplmr1 = rhpdlm(i+1,ll,mm)*rhpdlm(i+1,ll+1,mm+1) + rhcdlm(i+1,ll,mm)*rhcdlm(i+1,ll+1,mm+1)
            Eplmi1 = rhpdlm(i+1,ll,mm)*rhcdlm(i+1,ll+1,mm+1) - rhpdlm(i+1,ll+1,mm+1)*rhcdlm(i+1,ll,mm)
            E0lmr1 = rhpdlm(i+1,ll,mm)*rhpdlm(i+1,ll,mm+1) + rhcdlm(i+1,ll,mm)*rhcdlm(i+1,ll,mm+1)
            E0lmi1 = rhpdlm(i+1,ll,mm)*rhcdlm(i+1,ll,mm+1) - rhcdlm(i+1,ll,mm)*rhpdlm(i+1,ll,mm+1)
            Emlmr1 = rhpdlm(i+1,ll,mm)*rhpdlm(i+1,ll-1,mm+1) + rhcdlm(i+1,ll,mm)*rhcdlm(i+1,ll-1,mm+1)
            Emlmi1 = rhpdlm(i+1,ll,mm)*rhcdlm(i+1,ll-1,mm+1) - rhcdlm(i+1,ll,mm)*rhpdlm(i+1,ll-1,mm+1)
	    Fplm = rhpdlm(i,ll,mm)*rhpdlm(i,ll+1,mm) + rhcdlm(i,ll,mm)*rhcdlm(i,ll+1,mm)
	    F0lm = rhpdlm(i,ll,mm)**2 + rhcdlm(i,ll,mm)**2
            Fplm1 = rhpdlm(i+1,ll,mm)*rhpdlm(i+1,ll+1,mm) + rhcdlm(i+1,ll,mm)*rhcdlm(i+1,ll+1,mm)
            F0lm1 = rhpdlm(i+1,ll,mm)**2 + rhcdlm(i+1,ll,mm)**2

            Px_GW = Px_GW + dto32pi*(cplm*(Eplmr+Eplmr1) + c0lm*(E0lmr+E0lmr1) + &
                              cmlm*(Emlmr+Emlmr1) )
            Py_GW = Py_GW + dto32pi*(cplm*(Eplmi+Eplmi1) + c0lm*(E0lmi+E0lmi1) + &
                              cmlm*(Emlmi+Emlmi1) )
	    Pz_GW = Pz_GW + dto32pi*(2.d0*dplm*(Fplm+Fplm1) + d0lm*(F0lm+F0lm1) )

         end do
      end do
      ! vx_GW, vy_GW, and vz_GW are in km/s. Speed of light c = 299792.458 km/s.
      vx_GW = Px_GW ! /(Madm-E_GW)*299792.458d0
      vy_GW = Py_GW ! /(Madm-E_GW)*299792.458d0
      vz_GW = Pz_GW ! /(Madm-E_GW)*299792.458d0
      write(1,'(7ES25.15)') tret(1)+i*dt,E_GW,J_GW,sqrt(vx_GW**2+vy_GW**2+vz_GW**2),vx_GW,vy_GW,vz_GW
   end do
   close(1)

   !!! Output all GW modes to files with names h_l<lmode>_m<mmode><file suffix>
   !!do j=1,num_modes
   !!   call get_lm(j,l_gw,m_gw)
   !!   call int_to_char(l_gw,ch_l,1)
   !!   call int_to_char(abs(m_gw),ch_m,1)     
   !!   if (m_gw .lt. 0) then 
   !!      hphc_filename = 'h_l'//ch_l//'_m-'//ch_m//trim(file_suffix)
   !!      write(*,*) 'Outputing (',ch_l,',-',ch_m,') mode to file ',hphc_filename
   !!   else
   !!      hphc_filename = 'h_l'//ch_l//'_m'//ch_m//trim(file_suffix)
   !!      write(*,*) 'Outputing (',ch_l,',',ch_m,') mode to file ',hphc_filename
   !!   end if
   !!   open(1,file=hphc_filename,status='unknown')
   !!   do i=1,n
   !!      t = t0 + dt*(i-1)
   !!      if (t .ge. t_start .and. t .le. t_end) &
   !!         write(1,*) t,hp_plus_i_hc(j,2*i-1),hp_plus_i_hc(j,2*i)
   !!   end do
   !!   close(1)
   !!end do

   stop
   end 

! Compute (l,m) of GW mode from the count number n
subroutine get_lm(n,l,m)
  implicit none
  integer :: n,l,m,i
!
  l = 2
  m = 2
  do i=2,n
     m = m-1
     if (-m .gt. l) then 
        l = l+1
        m = l
     end if
  end do
end subroutine get_lm

! Numerical recipe FFT subroutine 
! NOTE: nn must be power of 2 
! For inverse transform (isign=-1), the result should be divided by nn
!
      SUBROUTINE four1(data,nn,isign)
      implicit none
      INTEGER :: isign,nn
      REAL*8 :: data(2*nn)
      INTEGER :: i,istep,j,m,mmax,n
      REAL*8 :: tempi,tempr
      REAL*8 :: theta,wi,wpi,wpr,wr,wtemp
!
      n=2*nn
      j=1
      do 11 i=1,n,2
        if(j.gt.i)then
          tempr=data(j)
          tempi=data(j+1)
          data(j)=data(i)
          data(j+1)=data(i+1)
          data(i)=tempr
          data(i+1)=tempi
        endif
        m=n/2
1       if ((m.ge.2).and.(j.gt.m)) then
          j=j-m
          m=m/2
        goto 1
        endif
        j=j+m
11    continue
      mmax=2
2     if (n.gt.mmax) then
        istep=2*mmax
        theta=6.283185307179586d0/(isign*mmax)
        wpr=-2.d0*sin(0.5d0*theta)**2
        wpi=sin(theta)
        wr=1.d0
        wi=0.d0
        do 13 m=1,mmax,2
          do 12 i=m,n,istep
            j=i+mmax
            tempr=wr*data(j)-wi*data(j+1)
            tempi=wr*data(j+1)+wi*data(j)
            data(j)=data(i)-tempr
            data(j+1)=data(i+1)-tempi
            data(i)=data(i)+tempr
            data(i+1)=data(i+1)+tempi
12        continue
          wtemp=wr
          wr=wr*wpr-wi*wpi+wr
          wi=wi*wpr+wtemp*wpi+wi
13      continue
        mmax=istep
      goto 2
      endif
      return
      END

! Convert an integer, n, to a character, ch, of length m. Note that n must be smaller 
! than 10**m.
!
    subroutine int_to_char(n,ch,m)
    implicit none
    integer n,m,i, itmp, d
    character(m) :: ch
!
    ch = ''
    itmp = n
    do i=m-1,1,-1
       d = int((itmp+0.01)/10**i)
       ch = ch(1:m-i-1)//achar(d+48)
       itmp = itmp - d*(10**i)
    end do
    ch = ch(1:m-1)//achar(itmp+48)
    end subroutine int_to_char

!-----------------------------------------------------------------------------
!
!  Numerical Recipe interpolation subroutine
!
!-----------------------------------------------------------------------------
!
      SUBROUTINE polint(xa,ya,n,x,y,dy)
      IMPLICIT NONE
      integer                    :: n,NMAX,i,m,ns
      real*8                     :: dy,x,y
      real*8, dimension(n)       :: xa,ya
      PARAMETER (NMAX=10)
      real*8, dimension(NMAX)    :: c,d
      real*8                     :: den,dif,dift,ho,hp,w
!
      ns=1
      dif=abs(x-xa(1))
      do 11 i=1,n
        dift=abs(x-xa(i))
        if (dift.lt.dif) then
          ns=i
          dif=dift
        endif
        c(i)=ya(i)
        d(i)=ya(i)
11    continue
      y=ya(ns)
      ns=ns-1
      do 13 m=1,n-1
        do 12 i=1,n-m
          ho=xa(i)-x
          hp=xa(i+m)-x
          w=c(i+1)-d(i)
          den=ho-hp
          if(den.eq.0.) then
            write(*,*) 'failure in polint'
            stop
          end if
          den=w/den
          d(i)=hp*den
          c(i)=ho*den
12      continue
        if (2*ns.lt.n-m)then
          dy=c(ns+1)
        else
          dy=d(ns)
          ns=ns-1
        endif
        y=y+dy
13    continue
      return
      END SUBROUTINE polint
