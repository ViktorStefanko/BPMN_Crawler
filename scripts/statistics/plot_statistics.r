make_bargraph_files_extensions <- function(csv_name, graph_name, pdf_name, x_lab, y_lab){
  pdf(paste(pdf_name, ".pdf"), width=6, height=8, paper='special')

  x <- read.csv(csv_name, row.names = 1, sep = ";", quote ='\"')

  my_bar <- barplot(x$Anzahl, ylim=c(0, max(x$Anzahl) + 700), names.arg = x$Dateiendung, col=rainbow(length(x$Anzahl)), border="black",
                      cex.names = 0.9, space = 0, main=graph_name, xlab=x_lab, ylab = y_lab)
  text(my_bar, x$Anzahl, labels=x$Anzahl, pos=3, cex=1)
  dev.off()
}
# make_bargraph_files_extensions('csv_files/extensions_of_files.csv', 'Balkendiagramm von Dateiendungen', 'diagrams/balk_diagr_dateiendungen', 'Dateiendung', 'Anzahl')


make_bargraph_languages <- function(csv_name, graph_name, pdf_name, x_lab, y_lab){
  pdf(paste(pdf_name, ".pdf"), width=6, height=8, paper='special')

  x <- read.csv(csv_name, row.names = 1, sep = ";", quote ='\"')
  my_bar <- barplot(x$Anzahl, ylim=c(0, max(x$Anzahl) + 100), names.arg = x$Programmiersprache, col=rainbow(length(x$Anzahl)), border="black",
                    main=graph_name, xlab=x_lab, ylab = y_lab, cex.names = 0.3, space = 0)
  text(my_bar, x$Anzahl, labels=x$Anzahl, pos=3, cex=1)
  dev.off()
}

#make_bargraph_languages('csv_files/languages_all_repos.csv', 'Programmiersprachen in allen Projekten', 'diagrams/balk_all_languages', 'Programmiersprachen', 'Anzahl')
#make_bargraph_languages('csv_files/languages_bpmn_repos.csv', 'Programmiersprachen in Projekten mit BPMN', 'diagrams/balk_bpmn_languages', 'Programmiersprachen', 'Anzahl')
#make_bargraph_languages('csv_files/languages_bpmn2_repos.csv', 'Programmiersprachen in Projekten mit BPMN2', 'diagrams/balk_bpmn2_languages', 'Programmiersprachen', 'Anzahl')
#make_bargraph_languages('csv_files/languages_xml_repos.csv', 'Programmiersprachen in Projekten mit XML', 'diagrams/balk_xml_languages', 'Programmiersprachen', 'Anzahl')
#make_bargraph_languages('csv_files/languages_png_repos.csv', 'Programmiersprachen in Projekten mit PNG', 'diagrams/balk_png_languages', 'Programmiersprachen', 'Anzahl')
#make_bargraph_languages('csv_files/languages_json_repos.csv', 'Programmiersprachen in Projekten mit JSON', 'diagrams/balk_json_languages', 'Programmiersprachen', 'Anzahl')

make_piechart <- function(csv_name, graph_name, pdf_name){
  pdf(paste(pdf_name, ".pdf"), width=6, height=8, paper='special')

  x <- read.csv('csv_files/extensions_of_files.csv', row.names = 1, sep = ";", quote ='\"')
  lbls <- x$Anzahl
  pct <- formatC(x$Prozentsatz, format="f", big.mark=",", digits=2)
  lbls <- paste(pct,"%",sep="")

  pie(x$Prozentsatz,labels = lbls, col=rainbow(length(lbls)), main=graph_name)
  legend("topright", legend=x$Dateiendung, cex = 0.75,
         fill = rainbow(length(lbls)))

  dev.off()
}

# make_piechart('csv_files/extensions_of_files.csv','Kreisdiagramm von Dateiendungen', 'diagrams/kreis_diagr_dateiendungen')
