! Compute E_GW and J_GW across a rectanglar surface
   implicit none
   integer :: nx,ny,nz,nmodes,lmax,i,j,ios,ntime,ncheck,nt
   integer :: l_gw,m_gw
   character*4 surface
   character*50 :: rhphc_filename,rhphcdot_filename
   real*8 :: E_GW,J_GW, Edot0,Edot1,Jdot0,Jdot1
   real*8 :: Madm,xmin,ymin,zmin,xmax,ymax,zmax,tstart,tend,dt,t
   integer, dimension(:), allocatable :: lmode,mmode
   real*8, dimension(:), allocatable :: tret_tab,tmp1,tmp2
   real*8, dimension(:,:,:), allocatable :: rhplm,rhclm,rhpdotlm,rhcdotlm
!
   open(1,file='gw_flux.input')
   read(1,*) 
   read(1,*) rhphc_filename,rhphcdot_filename,Madm,tstart,tend,dt
   read(1,*)
   read(1,*) nmodes,xmin,ymin,zmin,xmax,ymax,zmax
   read(1,*) 
   read(1,*) nx,ny,nz
   close(1)

   nt = int((tend-tstart)/dt + 1.d-10) + 1

   allocate( lmode(nmodes) )
   allocate( mmode(nmodes) )
   i = 2
   lmode(1) = 2
   mmode(1) = 2
   do
      do
          if (mmode(i-1) .eq. -lmode(i-1) .or. i .gt. nmodes) exit
          lmode(i) = lmode(i-1)
          mmode(i) = mmode(i-1)-1
          i = i+1
      end do
      if (i .gt. nmodes) exit
      lmode(i) = lmode(i-1)+1
      mmode(i) = lmode(i)
      i = i+1
   end do
   lmax = lmode(nmodes)

   ! Count the number of lines in rhphc_filename
   open(1,file=rhphc_filename,status='old')
   ntime = 0
   do
      read(1,*,iostat=ios) E_GW
      if (ios .ne. 0) exit 
      ntime = ntime +1
   end do
   close(1)

   write(*,*) 'Number of lines in ',trim(adjustl(rhphc_filename)),' is ',ntime

   ! Now check if the # of lines in rhphcdot_filename is the same as ntime
   open(1,file=rhphcdot_filename,status='old')
   ncheck = 0
   do
      read(1,*,iostat=ios) E_GW
      if (ios .ne. 0) exit
      ncheck = ncheck +1
   end do
   close(1)
   if (ncheck .ne. ntime) then 
      write(*,*) 'Error! The number of lines in ',trim(adjustl(rhphc_filename)),' is not the same as that in ',trim(adjustl(rhphcdot_filename))
      stop
   end if

   allocate(tmp1(2*nmodes+1))
   allocate(tmp2(2*nmodes+1))
   allocate(tret_tab(ntime))
   allocate(rhplm(ntime,lmax,-lmax:lmax))
   allocate(rhclm(ntime,lmax,-lmax:lmax))
   allocate(rhpdotlm(ntime,lmax,-lmax:lmax))
   allocate(rhcdotlm(ntime,lmax,-lmax:lmax))

   rhplm = 0.d0
   rhclm = 0.d0
   rhpdotlm = 0.d0
   rhcdotlm = 0.d0

   open(1,file=rhphc_filename,status='old')
   open(2,file=rhphcdot_filename,status='old')
   do i=1,ntime
      read(1,*) tmp1
      read(2,*) tmp2
      tret_tab(i) = tmp1(1)
      do j=1,nmodes
	 l_gw = lmode(j)
	 m_gw = mmode(j)
	 rhplm(i,l_gw,m_gw) = tmp1(2*j)
	 rhclm(i,l_gw,m_gw) = tmp1(2*j+1)
	 rhpdotlm(i,l_gw,m_gw) = tmp2(2*j)
         rhcdotlm(i,l_gw,m_gw) = tmp2(2*j+1)
      end do
   end do
   close(1)
   close(2)

   E_GW = 0.d0
   J_GW = 0.d0
   open(1,file='EJ_rect.dat',status='unknown')
   write(1,'("#   t         E_GW           J_GW")') 
   write(1,*) tstart,E_GW,J_GW
   call fluxes_EJ_6faces(tstart,Edot0,Jdot0,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
      rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime)
   !!call fluxes_EJ_1face(t,Edot0,Jdot0,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
   !!             rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime, &
   !!             'sphr')
   do i=1,nt
      t = tstart + i*dt
      call fluxes_EJ_6faces(t,Edot1,Jdot1,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
            rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime)
      !!call fluxes_EJ_1face(t,Edot1,Jdot1,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
      !!          rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime, & 
      !!          'sphr')
      E_GW = E_GW + dt*0.5d0*(Edot0 + Edot1)
      J_GW = J_GW + dt*0.5d0*(Jdot0 + Jdot1)
      write(1,*) t,E_GW,J_GW
      write(*,*) t,E_GW,J_GW
      !write(*,*) t,E_GW,Edot1
      Edot0 = Edot1 
      Jdot0 = Jdot1
   end do
   close(1)
 
   deallocate(lmode,mmode)
   deallocate(tret_tab,rhplm,rhclm,rhpdotlm,rhcdotlm,tmp1,tmp2)
   stop
   end

! Compute the energy and J fluxes through 6 rectanglar surfaces at coordinate time t
!
subroutine fluxes_EJ_6faces(t,E_flux,J_flux,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
                rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime)
  implicit none
  character*4 surface
  real*8 :: t,E_flux,J_flux,xmin,ymin,zmin,xmax,ymax,zmax,Madm
  integer :: nmodes,lmax,ntime, nx,ny,nz
  real*8, dimension(ntime) :: tret_tab
  real*8, dimension(ntime,lmax,-lmax:lmax) :: rhplm,rhclm,rhpdotlm,rhcdotlm
  integer, dimension(nmodes) :: lmode,mmode
  real*8 :: E_fluxi,J_fluxi
!
  surface = 'zmax'
  call fluxes_EJ_1face(t,E_flux,J_flux,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
     rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime,surface)

  surface = 'zmin'
  call fluxes_EJ_1face(t,E_fluxi,J_fluxi,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
     rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime,surface)

  E_flux = E_flux + E_fluxi
  J_flux = J_flux + J_fluxi

  surface = 'ymax'
  call fluxes_EJ_1face(t,E_fluxi,J_fluxi,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
     rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime,surface)

  E_flux = E_flux + E_fluxi
  J_flux = J_flux + J_fluxi

  surface = 'ymin'
  call fluxes_EJ_1face(t,E_fluxi,J_fluxi,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
     rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime,surface)

  E_flux = E_flux + E_fluxi
  J_flux = J_flux + J_fluxi

  surface = 'xmax'
  call fluxes_EJ_1face(t,E_fluxi,J_fluxi,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
     rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime,surface)

  E_flux = E_flux + E_fluxi
  J_flux = J_flux + J_fluxi

  surface = 'xmin'
  call fluxes_EJ_1face(t,E_fluxi,J_fluxi,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, &
     rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime,surface)

  E_flux = E_flux + E_fluxi
  J_flux = J_flux + J_fluxi
  
  end subroutine fluxes_EJ_6faces


! Compute the energy and J fluxes through one surface at coordinate time t
!
subroutine fluxes_EJ_1face(t,E_flux,J_flux,xmin,ymin,zmin,xmax,ymax,zmax,Madm,nx,ny,nz,tret_tab, & 
		rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime, & 
 	        surface)
  implicit none
  character*4 surface
  real*8 :: t,E_flux,J_flux,xmin,ymin,zmin,xmax,ymax,zmax,Madm
  integer :: nmodes,lmax,ntime, nx,ny,nz
  real*8, dimension(ntime) :: tret_tab
  real*8, dimension(ntime,lmax,-lmax:lmax) :: rhplm,rhclm,rhpdotlm,rhcdotlm
  integer, dimension(nmodes) :: lmode,mmode
  real*8 :: rhp,rhc,rhpdot,rhcdot,rhp_phi,rhc_phi, dA,r,x,y,z,tret,rstar,smx,small
  real*8 :: theta,phi, cth,sth, dx1,dx2,tmp
  integer :: n1,n2,i,j 
  real*8, parameter :: pi = 3.14159265358979323846d0
!
  if (surface .eq. 'zmax' .or. surface .eq. 'zmin') then 
     n1 = nx
     n2 = ny
     dx1 = (xmax-xmin)/nx
     dx2 = (ymax-ymin)/ny
     smx = zmax
     if (surface .eq. 'zmin') smx = zmin
  else if (surface .eq. 'ymax' .or. surface .eq. 'ymin') then 
     n1 = nx
     n2 = nz
     dx1 = (xmax-xmin)/nx
     dx2 = (zmax-zmin)/nz
     smx = ymax
     if (surface .eq. 'ymin') smx = ymin
  else if (surface .eq. 'xmax' .or. surface .eq. 'xmin') then 
     n1 = ny
     n2 = nz
     dx1 = (ymax-ymin)/ny
     dx2 = (zmax-zmin)/nz
     smx = xmax
     if (surface .eq. 'xmin') smx = xmin
  else if (surface .eq. 'sphr') then 
     ! Spherical surface with radius R = sqrt( zmax^2 + 2 |xmax ymax|/pi)
     n1 = nx
     n2 = ny
     dx1 = 2.d0/nx     ! delta cos(theta)
     dx2 = 2.d0*pi/ny  ! delta phi
     smx = sqrt( zmax*zmax + 2.d0*abs(xmax*ymax)/pi )
  else 
     write(*,*) 'Surface type not supported in fluxes_EJ_1face!'
     stop
  end if

  dA = dx1*dx2
  if (surface .eq. 'sphr') dA = smx*smx*dx1*dx2
  small = 1.d-5*min(dx1,dx2)

  E_flux = 0.d0
  J_flux = 0.d0

  do i=1,n1
     do j=1,n2
	if (surface .eq. 'zmax' .or. surface .eq. 'zmin') then
	   x = xmin + (i-0.5d0)*dx1
	   y = ymin + (j-0.5d0)*dx2
	   z = smx
	else if (surface .eq. 'ymax' .or. surface .eq. 'ymin') then
	   x = xmin + (i-0.5d0)*dx1
	   y = smx
	   z = zmin + (j-0.5d0)*dx2
	else if (surface .eq. 'xmax' .or. surface .eq. 'xmin') then
	   x = smx
	   y = ymin + (i-0.5d0)*dx1
	   z = zmin + (j-0.5d0)*dx2
        else if (surface .eq. 'sphr') then
	   cth = -1.d0 + (i-0.5d0)*dx1
	   sth = sqrt(1.d0-cth*cth)
  	   phi = (j-0.5d0)*dx2
   	   x = smx*sth*cos(phi)
	   y = smx*sth*sin(phi)
	   z = smx*cth
	end if
       
        ! Avoid coordinate singularity
        if (abs(x) + abs(y) .lt. small) x = small

	r = sqrt(x*x + y*y + z*z)
	rstar = r + 2.d0*Madm*log(0.5d0*r/Madm-1.d0)
	tret = t - rstar
        phi = atan2(y,x)
	theta = acos(z/r)

	call compute_rhphc_rhphcdot(tret,theta,phi,rhp,rhc,rhpdot,rhcdot,rhp_phi,rhc_phi, &
               tret_tab,rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime)

         E_flux = E_flux + (rhpdot*rhpdot + rhcdot*rhcdot)/(16.d0*pi) * dA * abs(smx)/r**3
         J_flux = J_flux - (rhp_phi*rhpdot + rhc_phi*rhcdot)/(16.d0*pi) * dA * abs(smx)/r**3
     end do
  end do

end subroutine fluxes_EJ_1face

! Compute rH, rHdot and rH_{,phi} at angles (theta, phi) and retarded time tret by 
! sum over modes.
subroutine compute_rhphc_rhphcdot(tret,theta,phi,rhp,rhc,rhpdot,rhcdot,rhp_phi,rhc_phi, & 
               tret_tab,rhplm,rhclm,rhpdotlm,rhcdotlm, nmodes,lmax,lmode,mmode,ntime)
  implicit none
  integer :: nmodes,ntime,lmax, l_gw,m_gw,i
  real*8, dimension(ntime) :: tret_tab
  real*8, dimension(ntime,lmax,-lmax:lmax) :: rhplm,rhclm,rhpdotlm,rhcdotlm
  integer, dimension(nmodes) :: lmode,mmode
  real*8 :: rhp,rhc,rhpdot,rhcdot,rhp_phi,rhc_phi, theta,phi,tret
  real*8 :: f1_int,f2_int,ym2lmr,ym2lmi
!  
  rhp = 0.d0
  rhc = 0.d0
  rhpdot = 0.d0
  rhcdot = 0.d0 
  rhp_phi = 0.d0
  rhc_phi = 0.d0
  do i=1,nmodes
     l_gw = lmode(i)
     m_gw = mmode(i)
     call ym2lm(l_gw,m_gw,theta,phi,ym2lmr,ym2lmi)
     if ( tret .lt. tret_tab(1) ) then 
        f1_int = 0.d0
	f2_int = 0.d0
     else
        call inter3(tret,f1_int,tret_tab,rhplm(:,l_gw,m_gw),ntime)
        call inter3(tret,f2_int,tret_tab,rhclm(:,l_gw,m_gw),ntime)
     end if
     rhp = rhp + f1_int*ym2lmr + f2_int*ym2lmi
     rhc = rhc - (f1_int*ym2lmi - f2_int*ym2lmr)
     rhp_phi = rhp_phi + m_gw*(f2_int*ym2lmr - f1_int*ym2lmi)
     rhc_phi = rhc_phi - m_gw*(f2_int*ym2lmi + f1_int*ym2lmr)
     if ( tret .lt. tret_tab(1) ) then
        f1_int = 0.d0
        f2_int = 0.d0
     else
        call inter3(tret,f1_int,tret_tab,rhpdotlm(:,l_gw,m_gw),ntime)
        call inter3(tret,f2_int,tret_tab,rhcdotlm(:,l_gw,m_gw),ntime)
     end if
     rhpdot = rhpdot + f1_int*ym2lmr + f2_int*ym2lmi
     rhcdot = rhcdot - (f1_int*ym2lmi - f2_int*ym2lmr)
  end do
end subroutine compute_rhphc_rhphcdot

! s=-2 spin-weighted spherical harmonics {}_{-2}Y_{lm}(theta,phi) = ym2lmr + i ym2lmi
subroutine ym2lm(l,m,theta,phi,ym2lmr,ym2lmi)
  implicit none
  integer :: l,m
  real*8 :: theta,phi,ym2lmr,ym2lmi,Wlmr,Wlmi,Xlmr,Xlmi
  real*8 :: cost,sint,Norm
!
  if (l .lt. 2) then 
     write(*,*) 'l must be greater than 1 in ym2lm!'
     stop
  end if
  cost = cos(theta)
  sint = sin(theta)
  call compute_Wlm_Xlm(l,m,cost,sint,phi,Wlmr,Wlmi,Xlmr,Xlmi)
  Norm = 1.d0/sqrt( (l-1.d0)*l*(l+1.d0)*(l+2.d0) )
  ym2lmr = Norm*(Wlmr + Xlmi/sint)
  ym2lmi = Norm*(Wlmi - Xlmr/sint)
end subroutine ym2lm

subroutine compute_Wlm_Xlm(l,m,cost,sint,ph,Wlmr,Wlmi,Xlmr,Xlmi)
  implicit none
  integer :: l,m
  real*8 :: th,ph
  real*8 :: cost,sint,cott,cosmp,sinmp,Plm,fac1,fac1_0,fac2,Pl1
  real*8 :: Plm1,Ylmr,Ylmi,Ylmtr,Ylmti,Wlmr,Wlmi,Xlmr,Xlmi,sig
  real*8 :: plgndr,factorial
  real*8, parameter :: PI = 3.14159265358979323846d0
!
  cott = cost/sint
  fac2 = sqrt( (2.D0*l+1.D0)*factorial(l-abs(m)) / ( 4.D0*PI*factorial(l+abs(m)) ) )
  fac1 = fac2 * (l+abs(m))*(l-abs(m)+1.d0)
  fac1_0 = sqrt( (2.D0*l+1.D0)/(4.d0*PI) )

  cosmp = cos( m * ph )
  sinmp = sin( m * ph )

  Plm = plgndr(l,abs(m),cost)

  if(m==0) then
     Pl1 = plgndr(l,1,cost)
     Ylmr = fac2*Plm
     Ylmtr = fac1_0 * Pl1
     Wlmr = -l*(l+1.D0)*Ylmr - 2.D0*cott*Ylmtr
     Xlmr = 0.D0
     Wlmi = 0.d0
     Xlmi = 0.d0
  else
     Plm1 = plgndr(l,abs(m)-1,cost)
     Ylmr = fac2*Plm
     Ylmtr = -fac1*Plm1 - abs(m)*cott*fac2*Plm
     if(m.lt.0) then
        sig = (-1.d0)**(mod(-m,2))
        Ylmr = Ylmr*sig
        Ylmtr = Ylmtr*sig
     end if

     Wlmr = ( -l*(l+1.d0)*Ylmr -2.d0*cott*Ylmtr + 2.d0*Ylmr*(m/sint)**2 )
     Xlmr = 2.d0*(Ylmtr - cott*Ylmr)*m
     Wlmi = Wlmr * sinmp
     Xlmi = Xlmr*cosmp
     Wlmr = Wlmr*cosmp
     Xlmr = -Xlmr*sinmp
  end if
end subroutine compute_Wlm_Xlm

! Associated Legendre polynomial
  FUNCTION plgndr(l,m,x)
    IMPLICIT NONE
    INTEGER, INTENT(IN) :: l,m
    REAL*8, INTENT(IN) :: x
    REAL*8 :: plgndr
    INTEGER :: i,ll
    REAL*8 :: fact,pll,pmm,pmmp1,somx2
!
    if (m .lt. 0 .or. m .gt. l .or. abs(x) .gt. 1.d0) then 
       write(*,*) 'Argument(s) out of range in plgndr'
       stop
    end if
    pmm=1.D0
    if (m .gt. 0) then
       somx2=sqrt((1.D0-x)*(1.D0+x))
       fact = 1.D0
       do i=1,m
          pmm = pmm*(-fact*somx2)
          fact = fact + 2.D0
       end do
    end if
    if (l == m) then
       plgndr=pmm
    else
       pmmp1=x*(2*m+1)*pmm
       if (l == m+1) then
          plgndr=pmmp1
       else
          do ll=m+2,l
             pll=(x*(2*ll-1)*pmmp1-(ll+m-1)*pmm)/(ll-m)
             pmm=pmmp1
             pmmp1=pll
          end do
          plgndr=pll
       end if
    end if
  END FUNCTION plgndr

! Factorial
  FUNCTION factorial(n)
    implicit none
    integer :: i,n
    real*8 :: factorial

    factorial = 1.D0
    do i=2,n
       factorial = factorial * i
    end do

  END FUNCTION factorial

! This subroutine calculates a function f(x) from a tabulated data
! x_tab(i) and f_tab(i)=f(x_tab(i)) (i=1,2,...,n) via 3rd order Lagrange interpolation. 
! x_tab must be sorted in ascending order.
!
subroutine inter3(x,f,x_tab,f_tab,n)
   implicit none
   integer :: n,ist,i,j
   integer, parameter :: interpolation_order=4
   real*8 :: x,f,tmp
   real*8, dimension(n) :: x_tab,f_tab
   real*8, dimension(interpolation_order) :: xa,ya
   logical :: exit_do
!
   if (x .lt. x_tab(1) .or. x .gt. x_tab(n)) then
      write(*,*) 'Value of x out of data range in inter3!',x,x_tab(1),x_tab(n)
      stop
   end if

   exit_do = .false.
   do i=1,n
      if (x .le. x_tab(i)) then
         ist = i - 1 - interpolation_order/2
         ist = max(0,ist)
         ist = min(n-interpolation_order,ist)
         exit_do = .true.
      end if
      if (exit_do) exit
   end do

   do i=1,interpolation_order
      xa(i) = x_tab(i+ist)
      ya(i) = f_tab(i+ist)
   end do
   call polint(xa,ya,interpolation_order,x,f,tmp)

end subroutine inter3

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
