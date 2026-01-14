import { ethers } from "hardhat";

async function main() {
  console.log("🚀 Déploiement SimpleNFT (ESM)...");
  
  const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
  const simpleNFT = await SimpleNFT.deploy(
    "Simple NFT",
    "SNFT",
    "https://api.nftmarketplace.com/metadata/"
  );
  
  await simpleNFT.waitForDeployment();
  const address = await simpleNFT.getAddress();
  
  console.log(`✅ SimpleNFT déployé à : ${address}`);
  console.log(` • Nom : ${await simpleNFT.name()}`);
  console.log(` • Symbole : ${await simpleNFT.symbol()}`);
  console.log(` • Prochain Token ID : ${await simpleNFT.nextTokenId()}`);
  
  return address;
}

main().catch((error) => {
  console.error("💥 ERREUR :", error);
  process.exitCode = 1;
});
