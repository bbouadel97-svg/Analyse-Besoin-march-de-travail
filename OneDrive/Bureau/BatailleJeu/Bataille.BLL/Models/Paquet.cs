namespace Bataille.BLL.Models
{
    public class Paquet
    {
        public List<Carte> Cartes { get; private set; }

        public Paquet()
        {
            Cartes = new List<Carte>();
        }

        public void AjouterCarte(Carte carte)
        {
            Cartes.Add(carte);
        }

        public void Melanger()
        {
            if (Cartes.Count == 0)
                throw new InvalidOperationException("Le paquet est vide.");

            Random rng = new Random();
            int n = Cartes.Count;
            while (n > 1)
            {
                n--;
                int k = rng.Next(n + 1);
                Carte value = Cartes[k];
                Cartes[k] = Cartes[n];
                Cartes[n] = value;
            }
        }
    }
}
