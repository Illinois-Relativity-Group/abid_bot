def rotate(view, nsteps, frame_start, frame_end):
	print "in rotate"
	ctrig = view
	myViewNormal = ctrig.viewNormal

	x = myViewNormal[0]
	y = myViewNormal[1]

	r = math.sqrt(x*x + y*y)
	phase = math.atan2(y, x)
	
	print "frame start: " + str(frame_start) + "frame_end: " + str(frame_end)
	for i in range(frame_start, frame_end,1):
		phi = 2*math.pi*i/(nsteps - 1)

		ctrig.viewNormal = (r*math.cos(phase + phi) , r*math.sin(phase + phi), myViewNormal[2])

		SetView3D(ctrig)
		DrawPlots()
		SaveWindow()
	
print "rotating"
rotate(c2,tot_frames, frame_start, frame_end)


