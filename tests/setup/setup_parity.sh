# bash <(curl https://get.parity.io -L) -r stable
mkdir .parity-bin
cd .parity-bin
curl -O "https://d1h4xl4cr1h0mo.cloudfront.net/v1.11.7/x86_64-unknown-debian-gnu/parity"
chmod +x parity
echo "deb [trusted=yes] http://ftp.debian.org/debian testing main" > testing.list && sudo mv testing.list /etc/apt/sources.list.d/
sudo apt update
sudo apt-get -t testing install libstdc++6
curl -O "https://storage.googleapis.com/ether_sql/export_blocks_mainnet.rlp"
./parity import ./export_blocks_mainnet.rlp --tracing on
(./parity &)
