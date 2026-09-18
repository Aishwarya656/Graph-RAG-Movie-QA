import streamlit as st
from neo4j import GraphDatabase


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Graph RAG Movie QA",
    page_icon="🎬",
    layout="wide"
)


# ==========================================================
# NEO4J CONNECTION
# ==========================================================

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "MovieRAG@123"


@st.cache_resource
def get_driver():

    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(
            NEO4J_USER,
            NEO4J_PASSWORD
        )
    )


driver = get_driver()


# ==========================================================
# TEST CONNECTION
# ==========================================================

def test_connection():

    with driver.session() as session:

        result = session.run(
            "RETURN 'Neo4j Connected' AS message"
        )

        return result.single()["message"]


# ==========================================================
# QUERY: ACTORS OF MOVIE
# ==========================================================

def get_movie_actors(movie_name):

    query = """
    MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
    WHERE toLower(m.title) = toLower($movie)
    RETURN m.title AS movie,
           p.name AS actor,
           r.role AS role
    ORDER BY actor
    """

    with driver.session() as session:

        result = session.run(
            query,
            movie=movie_name
        )

        return [
            record.data()
            for record in result
        ]


# ==========================================================
# QUERY: MOVIES OF ACTOR
# ==========================================================

def get_actor_movies(actor_name):

    query = """
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    WHERE toLower(p.name) = toLower($actor)
    RETURN p.name AS actor,
           m.title AS movie
    ORDER BY movie
    """

    with driver.session() as session:

        result = session.run(
            query,
            actor=actor_name
        )

        return [
            record.data()
            for record in result
        ]


# ==========================================================
# QUERY: RECOMMEND MOVIES
# ==========================================================

def recommend_movies(movie_name):

    query = """
    MATCH (target:Movie)
    WHERE toLower(target.title) = toLower($movie)

    MATCH (actor:Person)-[:ACTED_IN]->(target)

    MATCH (actor)-[:ACTED_IN]->(recommended:Movie)

    WHERE recommended <> target

    RETURN recommended.title AS movie,
           count(actor) AS common_actors

    ORDER BY common_actors DESC, movie
    LIMIT 10
    """

    with driver.session() as session:

        result = session.run(
            query,
            movie=movie_name
        )

        return [
            record.data()
            for record in result
        ]


# ==========================================================
# USER INTERFACE
# ==========================================================

st.title(
    "🎬 Graph RAG Movie Question Answering System"
)

st.write(
    "A Neo4j knowledge graph based movie "
    "question answering and recommendation system."
)


# ==========================================================
# CONNECTION STATUS
# ==========================================================

try:

    message = test_connection()

    st.success(message)

except Exception as e:

    st.error(
        f"Neo4j connection failed: {e}"
    )


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Choose a module",
    [
        "🏠 Home",
        "🎭 Movie Actors",
        "🎬 Actor Movies",
        "⭐ Recommendations"
    ]
)


# ==========================================================
# HOME
# ==========================================================

if page == "🏠 Home":

    st.header("Graph RAG Movie Assistant")

    st.write(
        """
        This application uses a Neo4j movie knowledge
        graph as the retrieval backend.

        The current prototype supports:

        • Movie → Actor retrieval
        • Actor → Movie retrieval
        • Graph-based movie recommendations

        The next stage will add an LLM to convert natural
        language questions into grounded answers.
        """
    )

    st.subheader("Knowledge Graph")

    st.code(
        """
(Person)
    |
    | ACTED_IN
    ↓
(Movie)

Actor → Movie
Movie → Actor
Movie → Recommended Movie
        """,
        language="text"
    )


# ==========================================================
# MOVIE ACTORS
# ==========================================================

elif page == "🎭 Movie Actors":

    st.header("🎭 Actors in a Movie")

    movie = st.text_input(
        "Enter movie title:",
        placeholder="Sudden Death"
    )

    if st.button(
        "Find Actors",
        type="primary"
    ):

        if not movie.strip():

            st.warning(
                "Please enter a movie title."
            )

        else:

            results = get_movie_actors(
                movie
            )

            if results:

                st.success(
                    f"Found {len(results)} actor record(s)."
                )

                for result in results:

                    st.write(
                        f"**{result['actor']}**"
                    )

                    if result.get("role"):

                        st.caption(
                            f"Role: {result['role']}"
                        )

            else:

                st.warning(
                    "Movie not found in the graph."
                )


# ==========================================================
# ACTOR MOVIES
# ==========================================================

elif page == "🎬 Actor Movies":

    st.header("🎬 Movies by Actor")

    actor = st.text_input(
        "Enter actor name:",
        placeholder="Tom Hanks"
    )

    if st.button(
        "Find Movies",
        type="primary"
    ):

        if not actor.strip():

            st.warning(
                "Please enter an actor name."
            )

        else:

            results = get_actor_movies(
                actor
            )

            if results:

                st.success(
                    f"Found {len(results)} movie(s)."
                )

                for result in results:

                    st.write(
                        f"🎬 {result['movie']}"
                    )

            else:

                st.warning(
                    "Actor not found in the graph."
                )


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

elif page == "⭐ Recommendations":

    st.header("⭐ Movie Recommendations")

    movie = st.text_input(
        "Enter a movie:",
        placeholder="Sudden Death"
    )

    if st.button(
        "Recommend Movies",
        type="primary"
    ):

        if not movie.strip():

            st.warning(
                "Please enter a movie title."
            )

        else:

            results = recommend_movies(
                movie
            )

            if results:

                st.success(
                    f"Found {len(results)} recommendation(s)."
                )

                for i, result in enumerate(
                    results,
                    start=1
                ):

                    st.write(
                        f"**{i}. {result['movie']}**"
                    )

                    st.caption(
                        "Common actors: "
                        f"{result['common_actors']}"
                    )

            else:

                st.warning(
                    "No recommendations found."
                )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Graph RAG Movie QA | Neo4j + Cypher + Streamlit"
)