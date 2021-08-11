# This script is meant for use on Ubuntu.
# It probably works on other distributions of Linux, but I have not tested compatibility.

if ! command -v git &> /dev/null
then
  echo "Git is not installed."
  echo "Installing git..."
  sudo apt install git
fi
echo "Git is installed. Continuing..."

if ! command -v pip3 &> /dev/null
then
  echo "Pip for Python 3 is not installed."
  echo "Installing pip for Python 3..."
  sudo apt install python3-pip
fi
echo "Pip for Python 3 is installed. Continuing..."

if ! command -v docker &> /dev/null
then
  echo "Docker is not installed."
  echo "Installing docker..."
  sudo snap install docker
fi
echo "Docker is installed. Continuing..."

echo "Downloading repository..."
git clone https://github.com/waitblock/LinkCheckerBot

# rename folder to start with a lowercase letter for docker
mv LinkCheckerBot link-checker-bot

# create a file for the token
touch link-checker-bot/src/TOKEN

echo "Downloading dependencies..."
pip3 install discord==1.7.3 requests==2.21.0

