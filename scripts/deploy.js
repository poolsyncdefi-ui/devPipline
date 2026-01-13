import hre from "hardhat";

async function main() {
  console.log("🚀 Déploiement SimpleNFT (ESM)...");
  
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
  
  // Vérification Etherscan (uniquement pour réseaux réels)
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\n⏳ Attente de 30s avant vérification...");
    await new Promise(resolve => setTimeout(resolve, 30000));
    
    try {
      await hre.run("verify:verify", {
        address: address,
        constructorArguments: [
          "Simple NFT",
          "SNFT",
          "https://api.nftmarketplace.com/metadata/"
        ]
      });
      console.log("✅ Contrat vérifié sur Etherscan");
    } catch (error) {
      if (error.message.includes("Already Verified")) {
        console.log("ℹ️  Contrat déjà vérifié");
      } else {
        console.log("⚠️  Échec vérification:", error.message);
      }
    }
  }
  
  return address;
}

main().catch((error) => {
  console.error("💥 ERREUR:", error);
  process.exitCode = 1;
});
