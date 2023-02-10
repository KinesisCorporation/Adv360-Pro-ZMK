#i get into some weird issues if i even touch this files from windows
#this script just nukes the file and redowwnloads it which i can do within WSL
cd bin
rm build.sh
curl -o build.sh https://raw.githubusercontent.com/AlexGirardDev/Adv360-Pro-ZMK/V2.0/bin/build.sh
sudo chmod +x build.sh
sudo chmod 777 build.shkk
