// scripts/deploy.js - Version CommonJS
const hre = require("hardhat");

async function main() {
  console.log("🚀 Déploiement SimpleNFT...");
  
  const SimpleNFT = await hre.ethers.getContractFactory("SimpleNFT");
  const simpleNFT = await SimpleNFT.deploy(
    "Simple NFT",
    "SNFT",
    "https://api.nftmarketplace.com/metadata/"
  );
  
  await simpleNFT.waitForDeployment();
  const address = await simpleNFT.getAddress();
  
  console.log(`✅ SimpleNFT déployé à: ${address}`);
  console.log(` • Name: ${await simpleNFT.name()}`);
  console.log(` • Symbol: ${await simpleNFT.symbol()}`);
}

main().catch((error) => {
  console.error("💥 ERREUR:", error);
  process.exitCode = 1;
});