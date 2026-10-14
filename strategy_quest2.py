
import streamlit as st
import random

st.set_page_config(
    page_title="City Economic Development Game",
    page_icon="",
    layout="centered"
)

# -----------------------------------------
# STRATEGIES AND SCORING
# -----------------------------------------

STRATEGIES = {
    "M": "Manufacturing Powerhouse",
    "P": "Productivity Engine",
    "G": "Global City Benchmark"
}

WEIGHTS = {
    "M": 1,
    "P": 6,
    "G": 36
}

MAX_QUESTIONS = 5

# -----------------------------------------
# QUESTIONS
# Each option is permanently linked to a
# strategy, regardless of displayed order.
# -----------------------------------------

QUESTIONS = [
    {
        "question": (
            "A city has limited funds for economic "
            "development. Where should it invest first?"
        ),
        "options": [
            {
                "strategy": "M",
                "text": (
                    "Develop serviced industrial areas and "
                    "strengthen connections between production "
                    "centres, suppliers and markets."
                )
            },
            {
                "strategy": "P",
                "text": (
                    "Address bottlenecks in transport, utilities "
                    "and digital infrastructure that increase "
                    "costs for businesses across the city."
                )
            },
            {
                "strategy": "G",
                "text": (
                    "Identify proven approaches from leading "
                    "cities and adapt them to improve infrastructure, "
                    "public spaces and urban service standards."
                )
            }
        ]
    },
    {
        "question": (
            "A major employer is considering investing in the "
            "city. Which advantage should the city focus on offering?"
        ),
        "options": [
            {
                "strategy": "M",
                "text": (
                    "Offer industrial land, production infrastructure "
                    "and established supplier networks."
                )
            },
            {
                "strategy": "P",
                "text": (
                    "Offer lower operating costs, infrastructure "
                    "reliability and efficient business operations."
                )
            },
            {
                "strategy": "G",
                "text": (
                    "Improve the urban environment, connectivity "
                    "and quality of services to meet the expectations "
                    "of leading business destinations."
                )
            }
        ]
    },
    {
        "question": (
            "Your city has high unemployment among young people. "
            "Which programme do you prioritise?"
        ),
        "options": [
            {
                "strategy": "M",
                "text": "Expand technical and vocational training."
            },
            {
                "strategy": "P",
                "text": (
                    "Improve digital, technical and management skills."
                )
            },
            {
                "strategy": "G",
                "text": (
                    "Develop education, mobility and urban amenities "
                    "based on leading cities that attract talent."
                )
            }
        ]
    },
    {
        "question": (
            "A city has many small and medium-sized businesses, "
            "but most remain informal or technologically outdated. "
            "What should it do?"
        ),
        "options": [
            {
                "strategy": "M",
                "text": (
                    "Strengthen local supplier networks and help "
                    "firms participate in larger production "
                    "and distribution chains."
                )
            },
            {
                "strategy": "P",
                "text": (
                    "Help businesses improve technology adoption, "
                    "workforce development and business processes."
                )
            },
            {
                "strategy": "G",
                "text": (
                    "Adapt institutional practices from leading "
                    "cities to support innovation and enterprise."
                )
            }
        ]
    },
    {
        "question": (
            "Which economic identity would you most like your "
            "city to develop over the next 20 years?"
        ),
        "options": [
            {
                "strategy": "M",
                "text": (
                    "A leading production centre known for industrial "
                    "output, manufacturing excellence and exports."
                )
            },
            {
                "strategy": "P",
                "text": (
                    "A highly efficient and innovative economy where "
                    "businesses across sectors generate greater value."
                )
            },
            {
                "strategy": "G",
                "text": (
                    "An internationally renowned city known for its "
                    "global role, talent and specialised services."
                )
            }
        ]
    }
]


# -----------------------------------------
# INITIALISE SESSION
# Shuffle once per session, not on every
# Streamlit rerun.
# -----------------------------------------

if "quiz_order" not in st.session_state:
    shuffled_questions = []

    for question in QUESTIONS:
        q = {
            "question": question["question"],
            "options": question["options"].copy()
        }
        random.shuffle(q["options"])
        shuffled_questions.append(q)

    st.session_state.quiz_order = shuffled_questions
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.finished = False


# -----------------------------------------
# RESET FUNCTION
# -----------------------------------------

def restart_quiz():
    for key in [
        "quiz_order",
        "current_question",
        "answers",
        "finished"
    ]:
        if key in st.session_state:
            del st.session_state[key]


# -----------------------------------------
# CALCULATE SCORES
# -----------------------------------------


def calculate_scores(answers):
    weights = {
        "M": 1,   # Manufacturing
        "P": 6,   # Productivity
        "G": 36   # Global Benchmark
    }

    counts = {"M": 0, "P": 0, "G": 0}
    raw_scores = {"M": 0, "P": 0, "G": 0}

    for strategy in answers.values():
        counts[strategy] += 1
        raw_scores[strategy] += weights[strategy]

    total_score = sum(raw_scores.values())

    return raw_scores, counts, total_score



# -----------------------------------------
# QUIZ SCREEN
# -----------------------------------------

st.title("What Kind of City Would You Build?")

st.write(
    "Make five decisions about the economic future "
    "of a city. Your choices will reveal your preferred "
    "economic development orientation."
)

if not st.session_state.finished:

    idx = st.session_state.current_question
    question = st.session_state.quiz_order[idx]

    st.progress((idx + 1) / MAX_QUESTIONS)
    st.caption(f"Question {idx + 1} of {MAX_QUESTIONS}")

    st.subheader(question["question"])

    # Store the selected strategy code, not the
    # displayed option position.
    option_lookup = {
        option["strategy"]: option["text"]
        for option in question["options"]
    }

    shuffled_codes = [
        option["strategy"] for option in question["options"]
    ]

    existing_answer = st.session_state.answers.get(idx)

    with st.form(key=f"question_form_{idx}"):

        selected = st.radio(
            "Choose one option:",
            options=shuffled_codes,
            format_func=lambda code: option_lookup[code],
            index=(
                shuffled_codes.index(existing_answer)
                if existing_answer in shuffled_codes
                else None
            ),
            key=f"selection_{idx}"
        )

        submitted = st.form_submit_button(
            "See results" if idx == MAX_QUESTIONS - 1
            else "Next question",
            use_container_width=True
        )

    if submitted:
        if selected is None:
            st.warning("Please select an option to continue.")
        else:
            st.session_state.answers[idx] = selected

            if idx == MAX_QUESTIONS - 1:
                st.session_state.finished = True
            else:
                st.session_state.current_question += 1

            st.rerun()


    
# -----------------------------------------
# RESULT PROFILE BASED ON TOTAL SCORE
# -----------------------------------------

if st.session_state.finished:

    # Ensure all five questions are answered
    if len(st.session_state.answers) != 5:
        st.warning("Please complete all five questions.")
        st.stop()

    # Calculate scores
    raw, counts, percentages = calculate_scores(
        st.session_state.answers
    )

    total_score = sum(raw.values())

    # -----------------------------------------
    # RESULT PROFILES
    # -----------------------------------------

    RESULT_PROFILES = {
        5: (
            "You envision your city as a Manufacturing Powerhouse!",
            "Driven by industrial growth, strong supply chains "
            "and employment generation."
        ),
        10: (
            "You envision your city as a Manufacturing Powerhouse!",
            "Driven by industrial growth, strong supply chains "
            "and employment generation."
        ),
        40: (
            "You envision your city as a Manufacturing Powerhouse!",
            "Driven by industrial growth, strong supply chains "
            "and employment generation."
        ),
        15: (
            "You envision your city as a Manufacturing Powerhouse "
            "with a Productivity Push!",
            "Your primary focus is manufacturing, complemented "
            "by efforts to improve skills, efficiency and business performance."
        ),
        45: (
            "You envision your city primarily as a Manufacturing Powerhouse!",
            "Manufacturing leads your vision, with some emphasis on "
            "productivity and learning from leading global cities."
        ),
        75: (
            "You envision your city as a Manufacturing Powerhouse "
            "with Global Ambitions!",
            "Your focus is industrial growth, complemented by "
            "aspirations to meet the standards of leading global cities."
        ),

        20: (
            "You envision your city as a Productivity Engine "
            "with a Manufacturing Focus!",
            "Your primary focus is improving efficiency and value creation, "
            "supported by a strong manufacturing base."
        ),
        25: (
            "You envision your city as a Productivity Engine!",
            "Driven by innovation, improved efficiency and "
            "higher value creation across sectors."
        ),
        30: (
            "You envision your city as a Productivity Engine!",
            "Driven by innovation, improved efficiency and "
            "higher value creation across sectors."
        ),
        55: (
            "You envision your city primarily as a Productivity Engine!",
            "Productivity is at the centre of your vision, with "
            "some emphasis on manufacturing and global benchmarks."
        ),
        60: (
            "You envision your city as a Productivity Engine!",
            "Driven by innovation, improved efficiency and "
            "higher value creation across sectors."
        ),
        90: (
            "You envision your city as a Productivity Engine "
            "with Global Ambitions!",
            "Your focus is economic efficiency and value creation, "
            "complemented by aspirations to meet global standards."
        ),

        110: (
            "You envision your city as a Global Benchmark "
            "with a Manufacturing Focus!",
            "Your vision draws on leading global cities while "
            "emphasising industrial growth and production capabilities."
        ),
        115: (
            "You envision your city primarily as a Global Benchmark!",
            "Inspired by leading global cities and their standards "
            "of infrastructure, governance, quality of life "
            "and economic competitiveness."
        ),
        120: (
            "You envision your city as a Global Benchmark "
            "with a Productivity Push!",
            "Your vision draws on leading global cities, with "
            "an emphasis on efficiency, innovation and value creation."
        ),
        145: (
            "You envision your city as a Global Benchmark!",
            "Inspired by leading global cities and their standards "
            "of infrastructure, governance, quality of life "
            "and economic competitiveness."
        ),
        150: (
            "You envision your city as a Global Benchmark!",
            "Inspired by leading global cities and their standards "
            "of infrastructure, governance, quality of life "
            "and economic competitiveness."
        ),
        180: (
            "You envision your city as a Global Benchmark!",
            "Inspired by leading global cities and their standards "
            "of infrastructure, governance, quality of life "
            "and economic competitiveness."
        ),

        50: (
            "You envision a city that combines all three strategies!",
            "Your choices reflect a mix of manufacturing, productivity "
            "improvements and global-city aspirations, without one "
            "clear development vision."
        ),
        80: (
            "You envision a city that combines all three strategies!",
            "Your choices reflect a mix of manufacturing, productivity "
            "improvements and global-city aspirations, without one "
            "clear development vision."
        ),
        85: (
            "You envision a city that combines all three strategies!",
            "Your choices reflect a mix of manufacturing, productivity "
            "improvements and global-city aspirations, without one "
            "clear development vision."
        ),
    }

    # -----------------------------------------
    # DISPLAY PERSONALised RESULT
    # -----------------------------------------

    if total_score not in RESULT_PROFILES:
        st.error(
            f"Unexpected total score: {total_score}. "
            "Please check the scoring logic."
        )
        st.stop()

    headline, description = RESULT_PROFILES[total_score]

    st.divider()

    st.markdown(
        f"<h2 style='text-align:center'>{headline}</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='text-align:center; font-size:1.15rem; "
        f"color:#888; line-height:1.6'>{description}</p>",
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # EXPLAIN ALL THREE STRATEGIES
    # -----------------------------------------

    st.divider()

    st.subheader("The three possible Strategies for your city")

    st.markdown(
        "**Manufacturing Powerhouse**  \n"
        "Focuses on expanding manufacturing output, developing "
        "industrial clusters, strengthening supply chains and logistics, "
        "and generating employment through production."
    )

    st.markdown(
        "**Productivity Engine**  \n"
        "Focuses on improving skills, technology, infrastructure "
        "and business processes to help firms across sectors "
        "generate greater value."
    )

    st.markdown(
        "**Global Benchmark**  \n"
        "Focuses on learning from leading global cities and adapting "
        "their approaches to infrastructure, governance, mobility, "
        "public services and quality of life to strengthen "
        "economic competitiveness."
    )

    # -----------------------------------------
    # PLAY AGAIN
    # -----------------------------------------

    st.divider()

    st.button(
        "Play again",
        on_click=restart_quiz,
        use_container_width=True
    )
