import { ethers } from "hardhat";

async function main() {
  // Adresses des contrats déployés (à remplacer par vos adresses)
  const SIMPLENFT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // Exemple Hardhat
  const LOCK_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"; // Exemple Hardhat
  
  console.log("🔄 Interaction avec les contrats...");
  
  // Récupérer les instances de contrat
  const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
  const simpleNFT = SimpleNFT.attach(SIMPLENFT_ADDRESS);
  
  const Lock = await ethers.getContractFactory("Lock");
  const lock = Lock.attach(LOCK_ADDRESS);
  
  // Informations SimpleNFT
  console.log("\n📊 SimpleNFT :");
  console.log(` • Nom : ${await simpleNFT.name()}`);
  console.log(` • Symbole : ${await simpleNFT.symbol()}`);
  console.log(` • Supply total : ${await simpleNFT.totalSupply()}`);
  console.log(` • Prochain token ID : ${await simpleNFT.nextTokenId()}`);
  
  // Informations Lock
  console.log("\n🔒 Lock :");
  console.log(` • Propriétaire : ${await lock.owner()}`);
  console.log(` • Temps de déverrouillage : ${await lock.unlockTime()}`);
  console.log(` • Solde : ${ethers.formatEther(await ethers.provider.getBalance(LOCK_ADDRESS))} ETH`);
}

main().catch((error) => {
  console.error("💥 ERREUR :", error);
  process.exitCode = 1;
});