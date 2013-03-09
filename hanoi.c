enum {
	 N = 2,
};

int peg_positions[N];

static void hanoi(int n, int src, int dst)
{
	int tmp = (0 + 1 + 2) - src - dst;

	if (n == 0) {
		peg_positions[n] = dst;
		return;
	}
	hanoi(n - 1, src, tmp);
	peg_positions[n] = dst;
	hanoi(n - 1, tmp, dst);
}

int main()
{
	hanoi(N - 1, 0, 2);
	return 0;
}
