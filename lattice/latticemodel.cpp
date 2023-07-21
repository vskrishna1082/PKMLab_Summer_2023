#include <algorithm>
#include <iostream>
#include <iomanip>
#include <random>
#include <vector>
#include <array>
using namespace std;

template <typename T, size_t I>
using array2d = array<array<T,I>,I>;

const int latticesize = 100;
const int samples = 10000;
const int n = latticesize*latticesize;

class Lattice 
{
    public:
    array2d<int, latticesize> lattice;
    array<int, n> linearlattice;
    struct index {int i; int j;};

    void fillWithConc(double phi)
    {
        int n_solute = phi*n;
        for (int i = 0; i < latticesize; i++) {
            for (int j = 0; j < latticesize; j++)
            {
                lattice[i][j] = 1;
                linearlattice[latticesize*i + j] = 1;
                if (latticesize*i+j < n_solute) {
                    lattice[i][j] = -1;
                    linearlattice[latticesize*i + j] = -1;
                }
            }
        }
    }

    void shuffleLattice(int seed = 0)
    {
        auto rng = default_random_engine { };
        rng.seed(seed);
        shuffle(begin(linearlattice), end(linearlattice), rng);
        for (int i = 0; i < latticesize; i++) {
            for (int j = 0; j < latticesize; j++)
            {
                lattice[i][j] = linearlattice[10*i + j];
            }
        }
    }

    void printLattice()
    {
        for (int i = 0; i<n; i++)
        {
            int x = i/10;
            int y = i%10;
            cout << setw(2) << lattice[x][y] << " ";
            if (y == 9) {
                cout << "\n";
            }
        }
    }

    /* get energy of particle at index (i,j,k) */
    double getLocalEnergy(struct index idx)
    {
        /* apply boundary conditions */
        int idxx_prev = (idx.i != 0) ? idx.i-1 : latticesize - 1;
        int idxx_next = (idx.i != latticesize - 1) ? idx.i+1 : 0;

        int idxy_prev = (idx.j != 0) ? idx.j-1 : latticesize - 1;
        int idxy_next = (idx.j != latticesize - 1) ? idx.j+1 : 0;

        int currParticle = lattice[idx.i][idx.j];
        return -currParticle*(lattice[idxx_prev][idx.j] +
                             lattice[idxx_next][idx.j] +
                             lattice[idx.i][idxy_prev] +
                             lattice[idx.i][idxy_next]);
    }
    double getTotalEnergy()
    {
        double totalEnergy = 0;
#pragma omp parallel for reduction(+:totalEnergy)
        for (int i = 0; i < n; i++) {
                struct index idx = {i/latticesize,i%latticesize};
                int Energy = getLocalEnergy(idx);
                totalEnergy += Energy;
            }
        return totalEnergy / 2;
    }
};

int main()
{
    Lattice mylattice;
    for (double conc=0.1; conc<1.0; conc+=0.1)
    {
        long sumE=0;
        mylattice.fillWithConc(conc);
        for (int i=0; i< samples; i++) {
            mylattice.shuffleLattice(i);
            int Elattice = mylattice.getTotalEnergy();
            sumE += Elattice;
        }
        cout << "Conc : " << conc << " ";
        cout << "Mean : " << (double) sumE/samples << "\n";
    }
}
