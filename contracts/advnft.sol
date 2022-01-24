// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract advnft is ERC721, VRFConsumerBase {
    uint256 public tokencounter;
    uint256 public fee;
    bytes32 public keyhash;

    enum BREED {
        PUG,
        SHIB,
        BERNARD
    }
    mapping(uint256 => BREED) public tokenidbreed;
    mapping(bytes32 => address) public request_id_to_sender;
    event requestNFT(bytes32 indexed requestID, address requester);
    event breedAssigned(uint256 tokenId, BREED breed);

    constructor(
        address _vrfCoordinator,
        uint256 _fee,
        bytes32 _keyhash,
        address _linktoken
    )
        public
        ERC721("twins", "KNFT")
        VRFConsumerBase(_vrfCoordinator, _linktoken)
    {
        fee = _fee;
        keyhash = _keyhash;
        tokencounter = 0;
    }

    function create(string memory tokenURI) public returns (bytes32) {
        bytes32 requestID = requestRandomness(keyhash, fee);
        request_id_to_sender[requestID] = msg.sender;
        emit requestNFT(requestID, msg.sender);
    }

    function fulfillRandomness(bytes32 requestID, uint256 random)
        internal
        override
    {
        BREED breed = BREED(random % 3);
        uint256 newtokenid = tokencounter;
        tokenidbreed[newtokenid] = breed;
        emit breedAssigned(newtokenid, breed);
        address owner = request_id_to_sender[requestID];
        _safeMint(owner, newtokenid);
        tokencounter = tokencounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId));
        _setTokenURI(tokenId, _tokenURI);
    }
}
