// See https://aka.ms/new-console-template for more informatio
using Bataille.BLL.Models;
// on va créer un JoueurHumain et un JoueurOrdinateur, puis les afficher
var joueurHumain = new JoueurHumain("Joe");
var joueurOrdinateur = new JoueurOrdinateur(2,"Bot");
Console.WriteLine("Tournoir Grande Chelem 2025 est bien crée !");
Console.WriteLine("Le joeur 1 est prêt à jouer !");
Console.WriteLine($"Joueur humain : {joueurHumain.Nom}, Id : {joueurHumain.Id}");
Console.WriteLine($"Joueur ordinateur : {joueurOrdinateur.Nom}, Id : {joueurOrdinateur.Id}");
// on va créer une Partie entre les deux joueurs
var partie = new Partie(1, joueurHumain, joueurOrdinateur);
Console.WriteLine($"Partie créée le {partie.Date} entre {partie.Joueur1.Nom} et {partie.Joueur2.Nom}");
// on va utiliser PaquetFactory pour obtenir 52 cartes
var paquet = PaquetFactory.CreerPaquet52();
Console.WriteLine($"Nombre de cartes dans le paquet : {paquet.Count}");
// on va créer Paquet et appeler la méthode Melanger()
var paquetMelange = new Paquet();
foreach (var carte in paquet)
{
    paquetMelange.AjouterCarte(carte);
}
paquetMelange.Melanger();
Console.WriteLine("Le paquet a été mélangé.");
// on va afficher une carte aléatoire du paquet mélangé
var random = new Random();
var carteAleatoire = paquetMelange.Cartes[random.Next(paquetMelange.Cartes.Count)];
Console.WriteLine($"Carte aléatoire du paquet mélangé : {carteAleatoire.Valeur} de {carteAleatoire.Couleur}");


