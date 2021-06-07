Bhdisk data occupies very little physical space, so a few of the standard things need to be changed.
I modified seedmaker.py so that the grid seeds for bh are closer to the bh. the default setting of this file is the same, but i included a comment that says what i was using for this case. you may change this as needed. Note that Stu and Milton mentioned possibly needing to change how these seeds are chosen since the bh may be precessing.

You will likely need to turn down the maxsteps in Stream_0.xml as well.

I added two view xmls. bhdisk_view_reg.xml and bhdisk_view_zoomin.xml.

I added a colortable bhdisk.ct that is called by the pseudocolor plot used for bhdisk. make sure to copy this to your ~/.visit folder

The two files that you will need to change most frequently are bhbh_pseudo.xml and bhdisk_iso.xml. These must be set in params in rho_pseudoXML and rho_isoXML respectively.

To run the bhdisk, you must change plot density as volume to 0 and plot density as iso to 1 in runSingle (or runBundle). This tells the scripts to use isosurfaces on pseudocolor plots instead of the ordinary volume plot clouds.

Isosurfaces plot surfaces that all have the same density (logrho). If you want to change settings on the shells themselves, you should change bhdisk_iso.xml. Here, you can control the value for each shell in the contour Vals variable. Simply specify what value you want for a shell. The opacity and color that are selected for each shell are chosen from the colortable file. If the minimum and maximum are -4 and 0 for the density variable, then setting a shell value at -1 will create a color three quarters up the colortable, which corresponds to position 0.75 in the colortable file.

If you want to edit colors (not recommended) or opacities, you need to change the alpha values for points in the colortable file. You will likely need to experiment with many shells and their opacities. For this to work, you probably need to create a point inside the colortable near each shell you want. If you do this, make sure the color for this point is what it would have been originally, since we do not want to change the colors themseles.

bhbh_pseudo.xml is not needed as much, but if you want to control the settings on the rendering or min, max values, you can check in here
