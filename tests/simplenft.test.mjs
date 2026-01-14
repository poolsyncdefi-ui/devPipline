import { expect } from "chai";
import { ethers } from "hardhat";

describe("SimpleNFT", function () {
  let simpleNFT;
  let owner, addr1, addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    
    const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
    simpleNFT = await SimpleNFT.deploy(
      "Test NFT",
      "TNFT",
      "https://api.test.com/metadata/"
    );
    
    await simpleNFT.waitForDeployment();
  });

  it("Devrait avoir le bon nom et symbole", async function () {
    expect(await simpleNFT.name()).to.equal("Test NFT");
    expect(await simpleNFT.symbol()).to.equal("TNFT");
  });

  it("Devrait permettre au propriétaire de miner gratuitement", async function () {
    await simpleNFT.ownerMint(addr1.address, "token1.json");
    expect(await simpleNFT.balanceOf(addr1.address)).to.equal(1);
  });

  it("Devrait avoir un prix de mint initial", async function () {
    expect(await simpleNFT.mintPrice()).to.equal(ethers.parseEther("0.01"));
  });
});
