import { ethers } from "hardhat";

async function main() {
  // Adresse du contrat déployé localement
  const SIMPLENFT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  
  console.log("🔄 Interaction avec SimpleNFT...");
  
  const [owner, user1] = await ethers.getSigners();
  const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
  const simpleNFT = SimpleNFT.attach(SIMPLENFT_ADDRESS);
  
  // 1. Vérifier les informations de base
  console.log("📊 Informations contrat:");
  console.log(` • Nom: ${await simpleNFT.name()}`);
  console.log(` • Symbole: ${await simpleNFT.symbol()}`);
  console.log(` • Supply total: ${await simpleNFT.totalSupply()}`);
  console.log(` • Prix mint: ${ethers.formatEther(await simpleNFT.mintPrice())} ETH`);
  
  // 2. Mint par le propriétaire (gratuit)
  console.log("\n🆕 Mint par propriétaire...");
  const tx1 = await simpleNFT.ownerMint(user1.address, "token-1.json");
  await tx1.wait();
  console.log(`✅ NFT minté pour ${user1.address}`);
  console.log(` • Balance user1: ${await simpleNFT.balanceOf(user1.address)}`);
  console.log(` • Token ID: ${await simpleNFT.nextTokenId()}`);
  
  // 3. Mint payant (simulé)
  console.log("\n💰 Mint payant (simulation)...");
  const mintCost = await simpleNFT.mintPrice();
  
  // Note: Pour tester vraiment, il faut envoyer des ETH
  console.log(` • Coût requis: ${ethers.formatEther(mintCost)} ETH`);
  console.log("ℹ️  Pour tester le mint payant, ajoutez des fonds au compte");
  
  // 4. Changer le prix
  console.log("\n🔧 Changement de prix...");
  const newPrice = ethers.parseEther("0.02");
  const tx2 = await simpleNFT.setMintPrice(newPrice);
  await tx2.wait();
  console.log(`✅ Nouveau prix: ${ethers.formatEther(await simpleNFT.mintPrice())} ETH`);
}

main().catch((error) => {
  console.error("💥 ERREUR:", error);
  process.exitCode = 1;
});
