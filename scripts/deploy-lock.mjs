import { ethers } from "hardhat";

async function main() {
  console.log("🔒 Déploiement du contrat Lock...");
  
  // Définir le temps de déverrouillage (1 heure dans le futur)
  const unlockTime = Math.floor(Date.now() / 1000) + 3600;
  
  const Lock = await ethers.getContractFactory("Lock");
  const lock = await Lock.deploy(unlockTime, {
    value: ethers.parseEther("0.01")
  });
  
  await lock.waitForDeployment();
  const address = await lock.getAddress();
  
  console.log(`✅ Lock déployé à l'adresse : ${address}`);
  console.log(` • Temps de déverrouillage : ${new Date(Number(unlockTime) * 1000).toLocaleString()}`);
  console.log(` • Propriétaire : ${await lock.owner()}`);
  console.log(` • Fonds verrouillés : ${ethers.formatEther(await ethers.provider.getBalance(address))} ETH`);
  
  return address;
}

main().catch((error) => {
  console.error("💥 ERREUR :", error);
  process.exitCode = 1;
});