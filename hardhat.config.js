import "@nomicfoundation/hardhat-ethers";
import * as dotenv from "dotenv";

dotenv.config();

const config = {
  solidity: "0.8.20",
  networks: {
    hardhat: {
      type: "edr-simulated"
    }
  }
};

export default config;
