#Created by Abid Khan
#Feb 5, 2015
#This code combines the gw frames and rho frames, sets the rho_frames to 50%
#opacity, and saves the images.
#To run this, copy the script below into the gimp console and run it.
# @Params
#	rho_dir: the images of the density frames. makes sure these frames are labeled rho_#.png, where # is frame number
#	gw_dir: the images of the gravitaional wave frames. These PNGs should be labeled gw_#.png, where # is frame number
#	out_dir: this must be a made director where you wish to store the combined frames.
#	num_imgs: The number of frames that are in rho_dir and gw_dir (they should be the same number)
# Note: remember to combine frames in the same time instance.

########################### USER INPUT ####################################################
root = "/home/colten1/Desktop/NSNS_high_align/bw_images/"
kind = "hplus"
rho_dir = root + "rho_dir/"
gw_dir = root + "gw_dir_" + kind +"/"
out_dir = root + "merged_" + kind + "/"
num_imgs = 1751
###########################################################################################

for i in range(0, num_imgs):
	rho_img = 'rho_' + str(i).zfill(5) + '.png'
	gw_img  = 'gw_' + str(i).zfill(5) + '.png'
	out_img = kind + '_merged_' + str(i).zfill(4) + '.png'
	image = pdb.gimp_file_load(gw_dir + gw_img, gw_dir + gw_img)
	layer = pdb.gimp_file_load_layer(image, rho_dir + rho_img)
	pdb.gimp_image_add_layer(image, layer, 0)
	pdb.plug_in_colortoalpha(image, layer, '#3776FF')
	pdb.plug_in_colortoalpha(image, layer, '#FFFFFF')
	pdb.gimp_layer_set_opacity(layer, 100)
	final = pdb.gimp_image_flatten(image)
	pdb.file_png_save_defaults(image, final, out_dir + out_img, out_dir + out_img)
	pdb.gimp_image_delete(image)


