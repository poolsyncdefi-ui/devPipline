const hre = require("hardhat");

async function main() {
  console.log("🚀 Déploiement SimpleNFT (Hardhat v3)...");
  
  const SimpleNFT = await hre.ethers.getContractFactory("SimpleNFT");
  const simpleNFT = await SimpleNFT.deploy(
    "Simple NFT",
    "SNFT",
    "https://api.nftmarketplace.com/metadata/"
  );
  
  // ✅ CORRECTION ICI : Utiliser waitForDeployment() au lieu de deployed()
  await simpleNFT.waitForDeployment();
  const address = await simpleNFT.getAddress();
  
  console.log(`✅ SimpleNFT déployé à: ${address}`);
  console.log(` • Name: ${await simpleNFT.name()}`);
  console.log(` • Symbol: ${await simpleNFT.symbol()}`);
  console.log(` • Base URI: ${await simpleNFT.baseURI()}`);
  
  return address;
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
