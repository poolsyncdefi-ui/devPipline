import { expect } from "chai";
import { ethers } from "hardhat";

describe("SimpleNFT Contract", function () {
  let simpleNFT;
  let owner, addr1, addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    
    const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
    simpleNFT = await SimpleNFT.deploy(
      "Test NFT Collection",
      "TNFT",
      "https://api.test.com/metadata/"
    );
    
    await simpleNFT.waitForDeployment();
  });

  it("Devrait avoir le bon nom et symbole", async function () {
    expect(await simpleNFT.name()).to.equal("Test NFT Collection");
    expect(await simpleNFT.symbol()).to.equal("TNFT");
  });

  it("Devrait permettre au propriétaire de miner gratuitement", async function () {
    await simpleNFT.ownerMint(addr1.address, "token-1.json");
    expect(await simpleNFT.balanceOf(addr1.address)).to.equal(1);
    expect(await simpleNFT.nextTokenId()).to.equal(1);
  });

  it("Devrait avoir un prix de mint initial correct", async function () {
    expect(await simpleNFT.mintPrice()).to.equal(ethers.parseEther("0.01"));
  });

  it("Devrait changer le prix de mint", async function () {
    const newPrice = ethers.parseEther("0.02");
    await simpleNFT.setMintPrice(newPrice);
    expect(await simpleNFT.mintPrice()).to.equal(newPrice);
  });
});
