bash <(curl https://get.parity.io -L) -r stable
echo "deb http://ftp.debian.org/debian testing main" > testing.list && sudo mv testing.list /etc/apt/sources.list.d/
sudo apt update
sudo apt-get -t testing install libstdc++6
curl -O https://storage.googleapis.com/ether_sql/export_blocks_mainnet.rlp
parity import ./export_blocks_mainnet.rlp --tracing on
