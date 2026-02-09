namespace Bataille.BLL.Models;
public class Partie(int id, Joueur joueur1, Joueur joueur2)
{
    public int Id { get; set; } = id;
    public DateTime Date { get; set; } = DateTime.Now;
    public Joueur Joueur1 { get; set; } = joueur1;
    public Joueur Joueur2 { get; set; } = joueur2;
    public Joueur? Vainqueur { get; set; } = null;
    public Partie(int id, Joueur joueur1, Joueur joueur2, DateTime date) : this(id, joueur1, joueur2)
    {
        Id = id;
        Date = DateTime.Now;
        Joueur1 = joueur1;
        Joueur2 = joueur2;
        Vainqueur = null;
    }
}
    