#a tool to help you find the folder name of corresponding folder num, also the other way
if [[ $1 =~ ^[0-9]+$ ]]; then
	find h5data/ -maxdepth 1 -name "3d_data*" | sort -V | sed "${1}q;d"
else
	find h5data/ -maxdepth 1 -name "3d_data*" | sort -V | awk "/${1}/{ print NR; exit }"
fi
