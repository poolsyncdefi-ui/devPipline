const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Lock Contract", function () {
  it("Should deploy Lock contract", async function () {
    const unlockTime = Math.floor(Date.now() / 1000) + 3600; // 1h dans futur
    
    const Lock = await ethers.getContractFactory("Lock");
    const lock = await Lock.deploy(unlockTime, {
      value: ethers.parseEther("0.01")
    });
    
    await lock.waitForDeployment();
    
    expect(await lock.owner()).to.equal(await ethers.provider.getSigner(0).getAddress());
  });
});
