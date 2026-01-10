const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleNFT Contract", function () {
  let SimpleNFT;
  let simpleNFT;
  let owner;
  let addr1;
  let addr2;
  let addrs;

  beforeEach(async function () {
    // Récupérer les signers
    [owner, addr1, addr2, ...addrs] = await ethers.getSigners();
    
    // Déployer le contrat
    SimpleNFT = await ethers.getContractFactory("SimpleNFT");
    simpleNFT = await SimpleNFT.deploy(
      "Simple NFT",
      "SNFT",
      "https://api.nftmarketplace.com/metadata/"
    );
    
    await simpleNFT.waitForDeployment();
  });

  describe("Déploiement", function () {
    it("Devrait avoir le bon nom et symbole", async function () {
      expect(await simpleNFT.name()).to.equal("Simple NFT");
      expect(await simpleNFT.symbol()).to.equal("SNFT");
    });

    it("Devrait définir le owner correctement", async function () {
      expect(await simpleNFT.owner()).to.equal(owner.address);
    });

    it("Devrait initialiser avec le bon baseURI", async function () {
      expect(await simpleNFT.baseURI()).to.equal(
        "https://api.nftmarketplace.com/metadata/"
      );
    });
  });

  describe("Minting", function () {
    it("Devrait permettre au owner de mint gratuitement", async function () {
      await simpleNFT.ownerMint(addr1.address, "token1.json");
      
      expect(await simpleNFT.ownerOf(0)).to.equal(addr1.address);
      expect(await simpleNFT.nextTokenId()).to.equal(1);
    });

    it("Devrait permettre le mint payant", async function () {
      const mintPrice = await simpleNFT.mintPrice();
      
      await simpleNFT.connect(addr1).safeMint(
        addr1.address, 
        "token1.json", 
        { value: mintPrice }
      );
      
      expect(await simpleNFT.ownerOf(0)).to.equal(addr1.address);
    });

    it("Devrait échouer si paiement insuffisant", async function () {
      const mintPrice = await simpleNFT.mintPrice();
      
      await expect(
        simpleNFT.connect(addr1).safeMint(
          addr1.address, 
          "token1.json", 
          { value: mintPrice - 1n }
        )
      ).to.be.revertedWith("Insufficient payment");
    });

    it("Devrait rembourser l'excédent", async function () {
      const mintPrice = await simpleNFT.mintPrice();
      const excessAmount = mintPrice + ethers.parseEther("0.005");
      
      const balanceBefore = await ethers.provider.getBalance(addr1.address);
      
      const tx = await simpleNFT.connect(addr1).safeMint(
        addr1.address, 
        "token1.json", 
        { value: excessAmount }
      );
      
      const receipt = await tx.wait();
      const gasUsed = receipt.gasUsed * receipt.gasPrice;
      
      const balanceAfter = await ethers.provider.getBalance(addr1.address);
      const expectedBalance = balanceBefore - mintPrice - gasUsed;
      
      // Tolérance pour les variations de gas
      expect(balanceAfter).to.be.closeTo(expectedBalance, ethers.parseEther("0.001"));
    });
  });

  describe("Burning", function () {
    beforeEach(async function () {
      await simpleNFT.ownerMint(addr1.address, "token1.json");
    });

    it("Devrait permettre au owner de brûler son NFT", async function () {
      await simpleNFT.connect(addr1).burn(0);
      
      await expect(simpleNFT.ownerOf(0)).to.be.reverted;
    });

    it("Devrait échouer si non-owner essaie de brûler", async function () {
      await expect(
        simpleNFT.connect(addr2).burn(0)
      ).to.be.revertedWith("Not owner nor approved");
    });
  });

  describe("Getters", function () {
    it("Devrait retourner le bon tokenURI", async function () {
      await simpleNFT.ownerMint(addr1.address, "token1.json");
      
      expect(await simpleNFT.tokenURI(0)).to.equal(
        "https://api.nftmarketplace.com/metadata/token1.json"
      );
    });

    it("Devrait supporter les interfaces ERC721", async function () {
      // ERC165 interface ID pour ERC721
      const erc721InterfaceId = "0x80ac58cd";
      expect(await simpleNFT.supportsInterface(erc721InterfaceId)).to.be.true;
    });
  });

  describe("Admin functions", function () {
    it("Devrait permettre au owner de changer le prix", async function () {
      const newPrice = ethers.parseEther("0.02");
      await simpleNFT.setMintPrice(newPrice);
      
      expect(await simpleNFT.mintPrice()).to.equal(newPrice);
    });

    it("Devrait échouer si non-owner essaie de changer le prix", async function () {
      const newPrice = ethers.parseEther("0.02");
      
      await expect(
        simpleNFT.connect(addr1).setMintPrice(newPrice)
      ).to.be.reverted;
    });

    it("Devrait permettre le withdraw des fonds", async function () {
      const mintPrice = await simpleNFT.mintPrice();
      
      // Mint pour ajouter des fonds
      await simpleNFT.connect(addr1).safeMint(
        addr1.address, 
        "token1.json", 
        { value: mintPrice }
      );
      
      const contractBalanceBefore = await ethers.provider.getBalance(
        await simpleNFT.getAddress()
      );
      const ownerBalanceBefore = await ethers.provider.getBalance(owner.address);
      
      // Withdraw
      const tx = await simpleNFT.withdraw();
      const receipt = await tx.wait();
      const gasUsed = receipt.gasUsed * receipt.gasPrice;
      
      const contractBalanceAfter = await ethers.provider.getBalance(
        await simpleNFT.getAddress()
      );
      const ownerBalanceAfter = await ethers.provider.getBalance(owner.address);
      
      expect(contractBalanceAfter).to.equal(0);
      expect(ownerBalanceAfter).to.be.closeTo(
        ownerBalanceBefore + contractBalanceBefore - gasUsed,
        ethers.parseEther("0.001")
      );
    });
  });
});