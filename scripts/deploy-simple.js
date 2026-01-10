const hre = require("hardhat");

async function main() {
  console.log("🚀 Déploiement du contrat SimpleNFT (Hardhat v2)...");
  
  // Récupérer le contrat - syntaxe v2
  const SimpleNFT = await hre.ethers.getContractFactory("SimpleNFT");
  
  // Déployer avec paramètres
  const simpleNFT = await SimpleNFT.deploy(
    "Simple NFT",
    "SNFT",
    "https://api.nftmarketplace.com/metadata/"
  );
  
  // Attendre le déploiement - syntaxe v2
  await simpleNFT.deployed();
  
  console.log(`✅ SimpleNFT déployé à: ${simpleNFT.address}`);
  console.log(`   • Name: ${await simpleNFT.name()}`);
  console.log(`   • Symbol: ${await simpleNFT.symbol()}`);
  
  return simpleNFT.address;
}

// Exécuter directement
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
