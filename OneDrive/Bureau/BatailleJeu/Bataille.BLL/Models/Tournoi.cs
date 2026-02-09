using System.Security.Cryptography.X509Certificates;

namespace Bataille.BLL.Models;
public class Tournoi
{
    public int Id { get; set; }
    public string Nom { get; set; } = "Grand Chelem 2025";
    public DateTime DateCreation { get; set; }
    public List<Partie> Parties { get; set; }
    public Tournoi(int id, string nom)
    {
        Id = id;
        Nom = nom;
        DateCreation = DateTime.Now;
        Parties = new List<Partie>();
    }
    public void AjouterPartie(Partie partie)
    {
        Parties.Add(partie);
    }
}
