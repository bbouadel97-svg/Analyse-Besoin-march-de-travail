namespace Bataille.BLL.Models;

public class JoueurHumain : Joueur 
{ 
    public JoueurHumain( string nom)        : base(0, nom) // Id est fixé à 0 pour les joueurs humains
    {
    }   
}


    
