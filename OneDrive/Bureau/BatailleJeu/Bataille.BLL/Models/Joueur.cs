namespace Bataille.BLL.Models
{
public abstract class Joueur
{  public int Id { get; set; }
    public string Nom { get; set; }
    public Queue<Carte> Main { get; set; }
    public int Score { get; set; }
    public Joueur(int id, string nom)
    {
        Id = id;
        Nom = nom;
        Main = new Queue<Carte>();
        Score = 0;
    }
    public virtual Carte? JouerCarte()
    {
        if (Main.Count > 0)
            return Main.Dequeue();
        return null;
    }
}
}
