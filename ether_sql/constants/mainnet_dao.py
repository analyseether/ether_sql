# https://raw.githubusercontent.com/ethereum/go-ethereum/5f55d95aea433ef97c48ae927835d833772350de/params/dao.go
from web3.utils.formatters import hex_to_integer
from eth_utils import to_checksum_address
from ether_sql.globals import get_current_session
from ether_sql.models import StateDiff


MAINNET_DAO_BLOCK = 1920000
MAINNET_DAO_TIMESTAMP = '2016-07-20T13:20:40'
DAO_REFUND_CONTRACT = "0xbf4ed7b27f1d666546e30d74d50d173d20bca754"


def add_dao_hardfork_state_diff():
    current_session = get_current_session()
    with current_session.db_session_scope():
        for dict_account in DAO_DRAIN_LIST:
            state_diff = StateDiff.add_state_diff(
                balance_diff=dict_account['balance_diff'],
                nonce_diff=None,
                code_from=None,
                code_to=None,
                address=to_checksum_address(dict_account['address']),
                transaction_hash=None,
                transaction_index=None,
                block_number=MAINNET_DAO_BLOCK,
                timestamp=MAINNET_DAO_TIMESTAMP,
                state_diff_type='dao-fork')
            current_session.db_session.add(state_diff)

DAO_DRAIN_LIST = [
    {'address': '0x253488078a4EdF4D6F42f113D1e62836A942Cf1a', 'balance_diff': -3486036451558542464},
    {'address': '0x9Ea779F907f0B315B364b0Cfc39A0FDE5b02a416', 'balance_diff': -15841461690131427090010},
    {'address': '0x200450F06520Bdd6C527622A273333384D870eFB', 'balance_diff': -1250001619314659344457},
    {'address': '0xD9aef3A1E38A39C16B31D1AcE71bCa8ef58D315B', 'balance_diff': -100000129545172747556},
    {'address': '0xB136707642A4EA12FB4BAE820F03d2562EBFF487', 'balance_diff': -7277385711515429122911683},
    {'address': '0x5D2b2E6fcBE3B11D26B525E085Ff818DAE332479', 'balance_diff': -5000006477258637377},
    {'address': '0x7602B46DF5390e432EF1c307d4F2c9Ff6D65Cc97', 'balance_diff': -369231179004682274248},
    {'address': '0xA2F1CcbA9395D7Fcb155bBA8BC92dB9BAFaeAde7', 'balance_diff': -5000006477258637377},
    {'address': '0xAcD87E28B0C9d1254E868B81Cba4cc20D9a32225', 'balance_diff': -207153967008322399135},
    {'address': '0x057B56736d32b86616a10F619859c6CD6F59092a', 'balance_diff': -9900012824972102},
    {'address': '0x0e0Da70933F4C7849fc0D203F5d1D43B9ae4532d', 'balance_diff': -19173240336954131945545},
    {'address': '0x84EF4b2357079CD7A7C69fD7a37cd0609a679106', 'balance_diff': -598974326560793095813484},
    {'address': '0xcc34673c6C40e791051898567A1222daF90Be287', 'balance_diff': -60000077727103648},
    {'address': '0x914d1B8B43e92723E64FD0a06F5BDB8Dd9b10C79', 'balance_diff': -285714295714285714286},
    {'address': '0xF4c64518EA10f995918A454158c6b61407EA345C', 'balance_diff': -269565591797974102411594},
    {'address': '0x35a051a0010aBA705c9008D7A7eff6FB88F6EA7B', 'balance_diff': -15276059789372406985},
    {'address': '0x542A9515200d14b68E934e9830d91645A980DD7A', 'balance_diff': -12548793143344641481996},
    {'address': '0xAC1ECAb32727358DbA8962a0F3b261731AAD9723', 'balance_diff': -1},
    {'address': '0x9f27DAEA7aca0AA0446220b98D028715E3Bc803D', 'balance_diff': -99998647723253121277},
    {'address': '0x440c59B325D2997A134c2c7c60a8c61611212BaD', 'balance_diff': -266854104538362875475},
    {'address': '0xE4AE1EfDfC53B73893aF49113D8694A057b9c0d1', 'balance_diff': -5000006477258637377},
    {'address': '0x9C15B54878Ba618f494B38F0Ae7443db6aF648bA', 'balance_diff': -2236999142516500888},
    {'address': '0x1cbA23d343A983e9b5cfd19496B9A9701ada385F', 'balance_diff': -68587370259945226},
    {'address': '0x6F6704E5a10332aF6672E50B3d9754Dc460DFa4D', 'balance_diff': -41173345768012804300},
    {'address': '0x2c19c7f9Ae8b751e37aEb2d93A699722395aE18F', 'balance_diff': -8519214441755701},
    {'address': '0xfE24Cdd8648121A43a7C86d289bE4dD2951ed49F', 'balance_diff': -269833661813680507459},
    {'address': '0x2a5ed960395e2a49B1c758CEF4aA15213cfd874c', 'balance_diff': -18693039890011849},
    {'address': '0x0737a6B837F97f46eBaDe41b9bC3e1c509C85c53', 'balance_diff': -7144077587762826223},
    {'address': '0xD4fE7Bc31cedB7BfB8A345F31e668033056B2728', 'balance_diff': -110000142499690430},
    {'address': '0x1Ca6aBD14D30aFfe533b24D7a21bff4C2D5e1F3B', 'balance_diff': -76761842290232377901},
    {'address': '0xBC07118b9aC290E4622f5e77A0853539789eFFbE', 'balance_diff': -5634097608979247392143},
    {'address': '0x6131c42Fa982E56929107413a9D526fD99405560', 'balance_diff': -2121837249362469256186},
    {'address': '0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413', 'balance_diff': -1200000000000000001},
    {'address': '0x0101F3Be8Ebb4BbD39A2e3B9A3639d4259832FD9', 'balance_diff': -559384955979606013894},
    {'address': '0xACcC230e8a6E5be9160b8CDF2864Dd2a001c28B6', 'balance_diff': -23997787866533545896},
    {'address': '0x782495B7B3355efB2833D56ecb34dc22AD7dFCC4', 'balance_diff': -250000323862931868891},
    {'address': '0xDA2FeF9e4a3230988ff17Df2165440f37e8B1708', 'balance_diff': -73722042576599901129491},
    {'address': '0x779543A0491a837Ca36CE8c635d6154E3C4911A6', 'balance_diff': -100000000000000000},
    {'address': '0xBf4eD7b27F1d666546E30D74d50d173d20bca754', 'balance_diff': 12001961845205763407115004},
    {'address': '0x5C8536898FBb74FC7445814902FD08422EaC56D0', 'balance_diff': -205100000000392887672},
    {'address': '0x5c6E67Ccd5849c0D29219c4F95F1a7a93b3F5dC5', 'balance_diff': -1},
    {'address': '0x4613f3bca5c44EA06337A9e439FBc6D42E501D0a', 'balance_diff': -28927603152430302650042},
    {'address': '0x4deb0033Bb26Bc534B197E61D19e0733e5679784', 'balance_diff': -1256101627216914882057},
    {'address': '0x6d87578288B6cb5549d5076A207456A1f6a63DC0', 'balance_diff': -1944767821345229848},
    {'address': '0xF14C14075d6C4Ed84B86798AF0956DEEf67365b5', 'balance_diff': -2123311222366559138},
    {'address': '0x319F70bAb6845585F412ec7724b744FEc6095C85', 'balance_diff': -90658},
    {'address': '0xD131637D5275fd1a68a3200f4aD25c71A2a9522E', 'balance_diff': -118886510785155274580},
    {'address': '0x06706dd3f2c9aBF0a21DDCc6941d9B86F0596936', 'balance_diff': -1428573279216753537},
    {'address': '0x1975BD06D486162d5DC297798DFC41EDD5D160a7', 'balance_diff': -989001281201758473335},
    {'address': '0xaEEb8fF27288BDABC0FA5EBb731B6f409507516c', 'balance_diff': -859189750496835322093},
    {'address': '0x3BA4D81DB016Dc2890C81F3AcEc2454BFf5AAda5', 'balance_diff': -1},
    {'address': '0x9dA397b9E80755301a3B32173283a91c0ef6c87E', 'balance_diff': -934889382511061152962},
    {'address': '0x21C7FDB9ED8D291D79fFD82EB2c4356Ec0D81241', 'balance_diff': -27428797178668633},
    {'address': '0xbCF899e6C7d9d5a215aB1e3444c86806FA854c76', 'balance_diff': -30696803822257124360133},
    {'address': '0x6B0c4d41Ba9ab8D8cFB5D379C69A612F2CEd8eCb', 'balance_diff': -854763543},
    {'address': '0x52C5317c848ba20C7504cB2c8052abD1Fde29D03', 'balance_diff': -1996002585721648041229},
    {'address': '0xD343B217DE44030AFAa275F54D31A9317c7F441e', 'balance_diff': -5192307692307692307692},
    {'address': '0x5524c55fb03cf21f549444cCbeCB664D0aCAd706', 'balance_diff': -6773243673260677597543},
    {'address': '0x807640A13483f8AC783c557fcDF27Be11ea4AC7A', 'balance_diff': -89472700},
    {'address': '0xD164B088bd9108B60D0ca3751DA4bceb207b0782', 'balance_diff': -1000001295451727475566},
    {'address': '0xd1ac8b1ef1b69Ff51D1D401a476e7e612414f091', 'balance_diff': -18387737083543350},
    {'address': '0x304a554a310C7e546dfe434669C62820b7D83490', 'balance_diff': -3642408527612792706899331},
    {'address': '0x51E0DDd9998364A2Eb38588679F0D2C42653E4A6', 'balance_diff': -10000012954517274755},
    {'address': '0x9fcD2deAff372A39cc679D5c5e4de7bafB0B1339', 'balance_diff': -1409336722195117395464},
    {'address': '0x492EA3bb0f3315521C31F273e565B868fC090F17', 'balance_diff': -367380383063135344585},
]
