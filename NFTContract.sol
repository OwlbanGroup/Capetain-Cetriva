// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CapetainCetrivaNFT is ERC721, Ownable {
    uint256 public nextTokenId;
    string public baseTokenURI;

    constructor(string memory _baseTokenURI) ERC721("CapetainCetrivaNFT", "CCTNFT") {
        baseTokenURI = _baseTokenURI;
    }

    function mint(address to) external onlyOwner {
        _safeMint(to, nextTokenId);
        nextTokenId++;
    }

    function ownerOfToken(uint256 tokenId) external view returns (address) {
        return ownerOf(tokenId);
    }

    function mintCoetusAppNFT(address fundAddress) external onlyOwner {
        _safeMint(fundAddress, nextTokenId);
        nextTokenId++;
    }

    function mintOwlbanGroupNFT(address fundAddress) external onlyOwner {
        _safeMint(fundAddress, nextTokenId);
        nextTokenId++;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseTokenURI;
    }
}
