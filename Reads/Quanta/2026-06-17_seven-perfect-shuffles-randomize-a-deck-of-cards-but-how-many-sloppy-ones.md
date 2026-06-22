# Seven Perfect Shuffles Randomize a Deck of Cards. But How Many Sloppy Ones?

**Source:** Quanta  
**Author:** John Pavlus  
**Date:** 2026-06-17  
**Link:** https://www.quantamagazine.org/seven-perfect-shuffles-randomize-a-deck-of-cards-but-how-many-sloppy-ones-20260617/

---

In 1992, mathematicians famously proved that [seven “riffle shuffles”](https://www.stat.berkeley.edu/~aldous/157/Papers/bayer_diaconis.pdf) — the kind where a player splits a deck of cards into two piles, then uses their thumbs to interleave them back together in a zipperlike motion — are enough to mix up the deck.

When [Dave Bayer](https://www.math.columbia.edu/~bayer/) and [Persi Diaconis](https://diaconis.ckirby.su.domains/) came up with this proof, they also revealed something surprising about what happens along the way: At first, the cards stay relatively orderly. But with that seventh shuffle, the deck suddenly tips into a highly unstructured state. This kind of behavior, called a cutoff phenomenon, is of interest beyond cards, and many dynamical systems — including “[spin glasses](https://www.quantamagazine.org/pioneering-climate-modelers-earn-nobel-prize-in-physics-20211005/)” in condensed matter physics — are [believed to exhibit it](https://cordis.europa.eu/project/id/101123174).

Unfortunately, Bayer and Diaconis’ proof — referred to by some as a mathematical miracle — only works if you adhere to some rigid constraints about how to cut and shuffle the deck. If you shuffle more like a middle schooler than a magician, the result doesn’t hold.

Now three mathematicians have finally [extended the finding](https://arxiv.org/abs/2510.22783) to less precise shuffles. [Mark Sellke](https://msellke.com/), a Harvard University statistician currently on leave to work at OpenAI, along with [Jialu Shi](https://jlsirh.faculty.bio/) and [Jiamin Wang](https://www.math.princeton.edu/people/jiamin-wang) (graduate students at the University of Cambridge and Princeton University, respectively), proved that a cutoff phenomenon exists for riffle shuffling even when you don’t cut the deck into two nice, even piles.

Diaconis was effusive about the update to his work. “It’s a fresh idea, and it’s remarkable that something like that would work as effectively as it does,” he said. “It’s a brilliant piece of mathematics.”

## **Mixing Cold Spots**

To call the humble riffle shuffle “complicated” sells it absurdly short. The number of possible arrangements for an ordinary deck of cards is 52 factorial — that is, 52 × 51 × 50 × … × 3 × 2 × 1, or (roughly speaking) an 8 followed by 67 zeros, close to the estimated number of atoms in our galaxy. Another way to put the figure into context: Every time you shuffle a deck of cards, you produce a configuration that has almost certainly never existed before, and never will again.

But mathematical interest in card shuffling goes beyond its combinatorial complexity. Back in 1981, Diaconis and Mehrdad Shahshahani [discovered cutoff phenomena](https://link.springer.com/article/10.1007/BF00535487) in the context of card shuffling — after which mathematicians started to uncover them all over the place.

Persi Diaconis ran away from home when he was 14 years old to work with a magician. He returned to school 10 years later and became a professional mathematician. Card tricks continue to play a role in his research.

Cutoffs are similar to [phase transitions](https://www.quantamagazine.org/tag/phase-transitions/) in physics, such as the sudden crystallization of liquid water into solid ice at zero degrees Celsius. But cutoffs occur in the specific mathematical context of “[Markov chains](https://www.quantamagazine.org/how-big-data-carried-graph-theory-into-new-dimensions-20210819/),” mathematical models that probabilistically describe how a system (like a deck of cards) moves between different configurations.

Cutoff phenomena, as their name suggests, happen in much the same way as Ernest Hemingway famously described going bankrupt: gradually, then suddenly. And while cutoffs are ubiquitous — they’re expected to occur in “most large, complex systems,” according to Sellke — it’s also hard to prove general theorems about them. “For most problems where one thinks there is a cutoff,” said [Laurent Saloff-Coste](https://math.cornell.edu/laurent-saloff-coste), a mathematician at Cornell University who has collaborated with Diaconis, “one doesn’t know how to prove it.”

That’s why the “seven shuffles are enough” theorem was such a big deal. Bayer and Diaconis — who as a teenager ran away from home to [apprentice with a magician specializing in card tricks](https://www.quantamagazine.org/persi-diaconis-mixes-math-and-magic-20150414/), before becoming a renowned mathematician — didn’t just prove the existence of a precise cutoff in a real-world system. They provided a single formula for where that cutoff should be, and that formula worked for decks of any size.

Yet terms and conditions also apply. One: The riffle shuffle has to follow a realistic but strict model where cards are randomly interleaved from the left or right pile one by one. (Each card gets dropped from either the left or the right pile with a probability that’s proportional to the number of cards remaining in that pile. This means that the cards don’t simply alternate between left and right, which would result in a predictable structure; instead, the order might go “left, right, right, left, right, left, left.”)

Two: The deck has to be cut more or less in half before shuffling.

“All of our analysis depends on those details,” Diaconis said.

In 1999, [Steven Lalley](https://galton.uchicago.edu/~lalley/), a mathematician at the University of Chicago, attempted to [loosen those constraints](https://www.stat.uchicago.edu/~lalley/Papers/GSRp.pdf) by seeking a cutoff proof for riffle shuffles that didn’t start with roughly evenly cut decks. “It seemed natural to me to ask — there are some people who tend to cut the deck a little higher or a little lower,” he said.

These less evenly cut decks have sets of cards that tend to stay in the same relative order even after multiple shuffles. While the rest of the deck looks well mixed, these particular sets of cards — which Lalley called “cold spots” — still retain information about their original locations in the deck.

Imagine, for instance, that you label your cards 1 through 52. After multiple shuffles, cards 16 and 17 will no longer appear right next to each other in the deck, but 16 might still tend to appear before 17 more often than it would in a random deck. If many pairs within a section of the original deck — say, cards 15 through 25 — show similar biases, then that set of cards forms a cold spot.

Lalley hoped to prove that when those cold spots disappeared, so would the last traces of order in the deck — giving him a way to show the existence of a cutoff.

But he couldn’t prove it.

## **Tracking Labels**

Two decades later, in 2019, the son of Lalley’s collaborator [Thomas Sellke](https://www.stat.purdue.edu/people/faculty/tsellke.html) — Mark, then a graduate student at Stanford University — found himself in one of Diaconis’ classes, where he learned about the original seven-shuffles result. “He mentioned offhandedly that if you don’t cut the deck in half, then nothing [about the proof] works anymore,” Mark Sellke recalled. “I was like, ‘This is it? … Come on, we must be able to do this.’”

By 2021, Mark Sellke had [pinpointed the cutoff](https://arxiv.org/abs/2103.05068) for decks cut much more unevenly than those in Bayer and Diaconis’ original work — including for decks cut into more than two piles. But the deck still had to be cut in the same way between each shuffle. He wanted a more realistic result, where the cuts from one shuffle to the next might look very different. And so in the summer of 2024, he teamed up with Shi and Wang, who had also expressed interest in the problem.

The trio first assigned each card a barcode. It starts when you cut the deck. All the cards in the left pile get assigned the number 1; those on the right, zero. Now shuffle, randomly interleaving the cards from the two piles one by one. Cut the deck again. If a card ends up in the left pile, add a 1 to its label; if it ends up in the right pile, add a zero.

As this process repeats through more riffle shuffles, each card builds up a longer and longer barcode of ones and zeros, which encodes its path through the shuffling process as it hops from left to right and back again. For instance, if the 17th card has a barcode of 0110 after four shuffles, that means it started in the right pile, ended up on the left twice, and then landed back on the right.

These numbers create a unique tracking label for every card in the deck. If two cards that started out in the same relative order — say, 16 and 17 — end up with the same barcode of ones and zeros, that means they took the exact same path through the shuffling process and are still in the same relative order.

To prove the presence of a cutoff, you have to show that very few of those matching barcodes remain after a certain number of shuffles — no matter how many cards you started with, or how the deck was cut. But comparing every barcode is time-consuming. Fortunately, the cold spots offer a shortcut, just as Lalley had hoped. Since those are the regions in the deck that tend to resist mixing, they’re the only places you have to check for barcodes that match.

Start with a deck of _n_ cards and list the barcodes of all the cards in the deck’s cold spots in ascending order.
