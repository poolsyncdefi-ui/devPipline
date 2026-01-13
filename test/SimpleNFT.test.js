const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleNFT", function () {
  let SimpleNFT, simpleNFT, owner, addr1;
  
  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    SimpleNFT = await ethers.getContractFactory("SimpleNFT");
    simpleNFT = await SimpleNFT.deploy(
      "Test NFT",
      "TNFT",
      "https://test.com/metadata/"
    );
    await simpleNFT.waitForDeployment();
  });
  
  it("Should have correct name and symbol", async function () {
    expect(await simpleNFT.name()).to.equal("Test NFT");
    expect(await simpleNFT.symbol()).to.equal("TNFT");
  });
  
  it("Should allow owner to mint", async function () {
    const tokenURI = "https://test.com/metadata/1.json";
    await simpleNFT.ownerMint(addr1.address, tokenURI);
    
    expect(await simpleNFT.ownerOf(0)).to.equal(addr1.address);
    expect(await simpleNFT.tokenURI(0)).to.equal(tokenURI);
  });
});
