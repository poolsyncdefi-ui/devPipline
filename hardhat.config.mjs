import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config = {
  solidity: {
    version: "0.8.19",
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
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./tests",  # Important: avec 's'
    cache: "./cache",
    artifacts: "./artifacts"
  }
};

export default config;
