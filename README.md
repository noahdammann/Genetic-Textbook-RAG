## Retrieval-Augmented Generation using OpenAI and Genetics Textbooks

### Overview

Retrieval-Augmented Generation (RAG) integrated with OpenAI's large langauge models (LLM). This approach gives the LLM context into specific domains of Genetics, in an effort to improve it's overall ability to answer genetics-based questions.

### Installation & Usage

1. Clone the repo
   ```sh
    git clone https://github.com/noahdammann/Genetic-Textbook-RAG
   ```
2. Move into traffic
   ```sh
    cd Genetic-Textbook-RAG
   ```
3. Install requirements
   ```sh
    pip3 install -r requirements.txt
   ```
4. Create .env file in root directory and set up environment variables. You will need an OPENAI and Pincecone account
   ```sh
    PINECONE_API_KEY=
    OPENAI_API_KEY=
   ```
5. Run the program. Note it will take about 10 minutes on the first run. Thereafter only about 30 seconds.
   ```sh
    python conceptual-approach.py
   ```

### Results

Here is example of asking a question that is specific to this textbook. You can test your own questions by changing the 'question' variable in each python program.

Question: Based on recent research on telomere shortening, what practical applications can be derived from the observed association between early childhood stress and telomere length, and how might this information influence public health strategies?

Augmented prompt generated:
```
Using the contexts below, answer the query.

    Contexts:
    When the children were 6 to 10 years old, the researchers collected samples of their DNA and measured the length of their telomeres. The results were striking: children who remained in the orphanages had significantly shorter telomeres than those who spent time in foster care. The researchers concluded that telomere length is affected by childhood adversity: children reared in stressful environments are more likely to have shorter telomeres than those raised in less stressful environments. Several other studies have found a similar association between telomere length in adults and early childhood stresses, such as abuse and chronic illness. How stress affects telomeres and results in their shortening is not known, but the research documents that chromosomes are more than just a repository of our genetic information: their structure is also affected by our environment.

    Think-pair-share
    Because telomeres become shorter with each cell division, much research has focused on determining if telomere length is indicative of biological aging. Although the relation between telomere length and aging is complex and not fully understood, considerable evidence suggests that telomeres do shorten with age, and that processes that lead to premature telomere shortening are associated with features of aging. In 2011, geneticists studying this phenomenon observed that hardships encountered early in life can play a part in shortening our telomeres.

    Query: Based on recent research on telomere shortening, what practical applications can be derived from the observed association between early childhood stress and telomere length, and how might this information influence public health strategies?
```

Output:
```
Recent research on telomere shortening has shown a clear association between early childhood stress and shorter telomeres. This information can have several practical applications in public health strategies. For instance, public health interventions could focus on reducing childhood stress through various means, such as improving access to mental health services for children and families, promoting supportive and nurturing environments, and implementing early intervention programs. By addressing early childhood stress, it may be possible to mitigate the negative effects on telomere length and potentially reduce the risk of age-related diseases and premature aging in the future. Additionally, raising awareness about the impact of childhood stress on telomere length could lead to policy changes that prioritize the well-being of children and families, ultimately contributing to better long-term health outcomes for individuals and communities.
```


### Textbooks

* Gene Control - David S. Latchman
* Genetics A Conceptual Approach - Benjamin A. Pierce
