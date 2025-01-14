// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CapetainCetrivaNFT is ERC721, Ownable {
    uint256 public nextTokenId;
    string public baseTokenURI;
    uint256 public constant MAX_TOKENS = 10000; // Set a maximum limit for tokens

    event Minted(address indexed to, uint256 tokenId); // Event for minting

    constructor(string memory _baseTokenURI) ERC721("CapetainCetrivaNFT", "CCTNFT") {
        baseTokenURI = _baseTokenURI;
    }

    function mint(address to) external onlyOwner {
        require(nextTokenId < MAX_TOKENS, "Max token limit reached"); // Check for max limit
        _safeMint(to, nextTokenId);
        emit Minted(to, nextTokenId); // Emit minting event
        nextTokenId++;
    }

    function ownerOfToken(uint256 tokenId) external view returns (address) {
        return ownerOf(tokenId);
    }

    function mintCoetusAppNFT(address fundAddress) external onlyOwner {
        require(nextTokenId < MAX_TOKENS, "Max token limit reached"); // Check for max limit
        _safeMint(fundAddress, nextTokenId);
        emit Minted(fundAddress, nextTokenId); // Emit minting event
        nextTokenId++;
    }

    function mintOwlbanGroupNFT(address fundAddress) external onlyOwner {
        require(nextTokenId < MAX_TOKENS, "Max token limit reached"); // Check for max limit
        _safeMint(fundAddress, nextTokenId);
        emit Minted(fundAddress, nextTokenId); // Emit minting event
        nextTokenId++;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseTokenURI;
    }
}
