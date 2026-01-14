// scripts/deploy.js - Version CommonJS
import { ethers } from "hardhat";

async function main() {
  console.log("🚀 Déploiement du contrat SimpleNFT...");
  
  const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
  const simpleNFT = await SimpleNFT.deploy(
    "Simple NFT",
    "SNFT",
    "https://api.nftmarketplace.com/metadata/"
  );
  
  await simpleNFT.waitForDeployment();
  const address = await simpleNFT.getAddress();
  
  console.log(`✅ SimpleNFT déployé à l'adresse : ${address}`);
  console.log(` • Nom : ${await simpleNFT.name()}`);
  console.log(` • Symbole : ${await simpleNFT.symbol()}`);
  console.log(` • URI de base : ${await simpleNFT.getBaseURI()}`);
  console.log(` • Propriétaire : ${await simpleNFT.owner()}`);
  
  return address;
}

main().catch((error) => {
  console.error("💥 ERREUR :", error);
  process.exitCode = 1;
});