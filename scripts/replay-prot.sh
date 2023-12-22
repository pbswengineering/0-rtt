RED='\033[0;31m'
WHITE='\033[1;37m'
GREEN='\033[1;32m'
NC='\033[0m'
echo -e "${WHITE}0-RTT ${RED}'retry-based'${WHITE} replay attack against a ${GREEN}protected${WHITE} server...${NC}"
python tls_playback.py --host 127.0.0.1 --port 444 --mode=protections