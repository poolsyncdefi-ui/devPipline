const hre = require("hardhat");

async function main() {
  console.log("🚀 Déploiement du contrat SimpleNFT...");
  
  // Récupérer le contrat
  const SimpleNFT = await hre.ethers.getContractFactory("SimpleNFT");
  
  // Déployer avec paramètres
  const simpleNFT = await SimpleNFT.deploy(
    "Simple NFT",          // name
    "SNFT",                // symbol
    "https://api.nftmarketplace.com/metadata/"  // baseURI
  );
  
  // Attendre le déploiement
  await simpleNFT.waitForDeployment();
  
  // Adresse du contrat déployé
  const address = await simpleNFT.getAddress();
  console.log(`✅ SimpleNFT déployé à: ${address}`);
  
  // Informations supplémentaires
  console.log(`   • Name: ${await simpleNFT.name()}`);
  console.log(`   • Symbol: ${await simpleNFT.symbol()}`);
  console.log(`   • Base URI: ${await simpleNFT.baseURI()}`);
  console.log(`   • Owner: ${await simpleNFT.owner()}`);
  
  // Vérification sur Etherscan (UNIQUEMENT pour les réseaux réels)
  if (hre.network.name !== "hardhat") {
    console.log(`\n🔍 Vérification sur Etherscan (${hre.network.name})...`);
    
    // Attendre quelques blocs pour que la transaction soit indexée
    console.log("   Attente de 30 secondes pour l'indexation...");
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
      console.log("✅ Contrat vérifié sur Etherscan!");
    } catch (error) {
      if (error.message.includes("Already Verified")) {
        console.log("✅ Contrat déjà vérifié");
      } else {
        console.log("⚠️  Échec vérification:", error.message);
      }
    }
  }
  
  return address;
}

// Fonction pour déployer sur différents réseaux
async function deployToNetwork(networkName) {
  console.log(`\n🌐 Déploiement sur ${networkName}...`);
  
  // Sauvegarder le réseau actuel
  const originalNetwork = hre.network.name;
  
  try {
    // Changer de réseau
    hre.changeNetwork(networkName);
    
    // Déployer
    const address = await main();
    
    // Sauvegarder l'adresse dans un fichier
    const fs = require("fs");
    const deploymentsDir = "./deployments";
    
    // CORRECTION : Créer le dossier seulement s'il n'existe pas
    if (!fs.existsSync(deploymentsDir)) {
      fs.mkdirSync(deploymentsDir, { recursive: true });
    }
    
    const deploymentInfo = {
      network: networkName,
      contract: "SimpleNFT",
      address: address,
      timestamp: new Date().toISOString(),
      deployer: (await hre.ethers.getSigners())[0].address
    };
    
    fs.writeFileSync(
      `${deploymentsDir}/${networkName}.json`,
      JSON.stringify(deploymentInfo, null, 2)
    );
    
    console.log(`💾 Informations sauvegardées: deployments/${networkName}.json`);
    
    return address;
    
  } catch (error) {
    console.error(`❌ Erreur déploiement sur ${networkName}:`, error.message);
    throw error;
  } finally {
    // Restaurer le réseau original
    hre.changeNetwork(originalNetwork);
  }
}

// Script principal
async function runDeployments() {
  console.log("=".repeat(60));
  console.log("        SCRIPT DE DÉPLOIEMENT NFT MARKETPLACE");
  console.log("=".repeat(60));
  
  const args = process.argv.slice(2);
  const network = args[0] || "hardhat";
  
  try {
    if (network === "all") {
      // Déployer sur tous les réseaux configurés
      const networks = ["hardhat", "sepolia", "mumbai"];
      
      for (const net of networks) {
        try {
          await deployToNetwork(net);
        } catch (error) {
          console.log(`⚠️  Skip ${net} due to error: ${error.message}`);
        }
      }
      
    } else {
      // Déployer sur un réseau spécifique
      await deployToNetwork(network);
    }
    
    console.log("\n🎉 Déploiement terminé avec succès!");
    
  } catch (error) {
    console.error("\n❌ Erreur pendant le déploiement:", error);
    process.exit(1);
  }
}

// Exécuter si appelé directement
if (require.main === module) {
  runDeployments()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
}

// Exporter pour usage dans d'autres scripts
module.exports = {
  main,
  deployToNetwork
};