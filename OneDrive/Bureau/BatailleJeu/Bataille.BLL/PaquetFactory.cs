using Bataille.BLL.Models;

public static class PaquetFactory
{
    public static List<Carte> CreerPaquet52()
    {
        var paquet = new List<Carte>();
        foreach (Couleur couleur in Enum.GetValues(typeof(Couleur)))
        {
            foreach (Valeur valeur in Enum.GetValues(typeof(Valeur)))
            {
                paquet.Add(new Carte(couleur, valeur));
            }
        }
        return paquet;
    }
}