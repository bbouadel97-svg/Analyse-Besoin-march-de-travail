namespace Bataille.BLL.Models
{
public class Carte
{
    public Couleur Couleur { get; }
    public Valeur Valeur { get; }
    public Carte(Couleur couleur, Valeur valeur)
    {
        Couleur = couleur;
        Valeur = valeur;
    }
    public override string ToString()
    {
        return $"{Valeur} de {Couleur}";
    }
}
}

