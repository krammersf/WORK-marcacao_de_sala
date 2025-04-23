function aplicarBordasPorSemana() {
    const folha = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("resumo");
    const dados = folha.getRange("A2:A").getValues();
    
    for (let i = 1; i < dados.length; i++) {
      const semanaAtual = Utilities.formatDate(new Date(dados[i][0]), Session.getScriptTimeZone(), "w");
      const semanaAnterior = Utilities.formatDate(new Date(dados[i - 1][0]), Session.getScriptTimeZone(), "w");
  
      if (semanaAtual !== semanaAnterior) {
        folha.getRange(i + 1, 1, 1, folha.getLastColumn()).setBorder(false, false, true, false, false, false);
      }
    }
  }