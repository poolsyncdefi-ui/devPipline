const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleNFT Contract", function () {
  let simpleNFT;
  let owner, addr1;
  
  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    
    const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
    simpleNFT = await SimpleNFT.deploy(
      "Test NFT",
      "TNFT",
      "https://api.test.com/metadata/"
    );
    
    await simpleNFT.waitForDeployment();
  });

  it("Should have correct name and symbol", async function () {
    expect(await simpleNFT.name()).to.equal("Test NFT");
    expect(await simpleNFT.symbol()).to.equal("TNFT");
  });

  it("Should allow owner to mint", async function () {
    await simpleNFT.ownerMint(addr1.address, "token1.json");
    expect(await simpleNFT.balanceOf(addr1.address)).to.equal(1);
  });
  
  it("Should return next token ID", async function () {
    expect(await simpleNFT.nextTokenId()).to.equal(0);
  });
});
