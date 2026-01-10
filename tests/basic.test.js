const { expect } = require("chai");

describe("Compilation test", function () {
  it("Should compile successfully", async function () {
    // Test simple pour vérifier que tout fonctionne
    expect(1 + 1).to.equal(2);
  });
  
  it("Should have web3 available", async function () {
    // Vérifier que web3 est disponible
    const Web3 = require("web3");
    const web3 = new Web3();
    expect(web3).to.exist;
  });
});
