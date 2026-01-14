// hardhat.config.js - Version CommonJS
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config = {
  solidity: {
    version: "0.8.19", // Compatible avec OpenZeppelin 4.9.5
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      chainId: 1337
	  type: "edr-simulated"  // <-- AJOUTÉ (obligatoire dans v3)
    },
     localhost: {
      url: "http://127.0.0.1:8545",
      type: "http"  // <-- AJOUTÉ (obligatoire dans v3)
    },
    sepolia: {
      url: process.env.ALCHEMY_API_KEY || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 11155111,
      type: "http"  // <-- AJOUTÉ (obligatoire dans v3)
    }
  },
  etherscan: {
    apiKey: {
      sepolia: process.env.ETHERSCAN_API_KEY || ""
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};

export default config;