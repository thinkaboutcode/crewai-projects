from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
from langchain_openai import ChatOpenAI

from custom_tools import SearchTools
from set_env import load_env

# make sure to provide your env
# os.environ["OPENAI_API_KEY"] = 'YOURS'
# and uncomment the following line, it loads my envs
load_env()

crewai_scrape_tool = ScrapeWebsiteTool()
custom_search_tool = SearchTools.web_search

# model_name='llama3-70b-8192',
# model_name='llama3-8b-8192' #best results so far
# model_name='mixtral-8x7b-32768' was not working for this usecase

llm = ChatOpenAI(
    # model_name='gpt-4',
    # model_name='llama3-8b-8192',
    temperature=1
)

sports_scout_agent = Agent(
    role='Sports Scout',
    goal='Finds out the key aspects of the sport you are interested in.',
    backstory='A person who always observes upcoming and tradional sport activities.',
    llm=llm,
    tools=[custom_search_tool, crewai_scrape_tool],
    allow_delegation=True,
    verbose=True
)

location_scout_agent = Agent(
    role='Location Scout',
    goal='Finds out the best location to execute specific a sport activity.',
    backstory="""A knowledgeable local expert who has extensive information \
        about all places where sport activities can be executed""",
    llm=llm,
    tools=[custom_search_tool, crewai_scrape_tool],
    allow_delegation=True,
    verbose=True
)

sports_coach_agent = Agent(
    role='Sports Coach',
    goal='Assists you in becoming the best as possible in your specific sport activity.',
    backstory='Has expertise in training other persons in their sport activities.',
    llm=llm,
    tools=[custom_search_tool, crewai_scrape_tool],
    allow_delegation=True,
    verbose=True
)

nutrition_expert_agent = Agent(
    role='Nutrition Expert',
    goal='Create a well formed nutrition plan to support a specific sports activity.',
    backstory='Has a strong background in nutrition and what is best to become stronger and healthier sportsman',
    llm=llm,
    tools=[custom_search_tool, crewai_scrape_tool],
    allow_delegation=True,
    verbose=True
)

mental_trainer_agent = Agent(
    role='Mental Trainer',
    goal='Creates a detailed plan how to develop mental toughness for a specific sport.',
    backstory='Knows about many mental trainings programs.',
    llm=llm,
    tools=[custom_search_tool, crewai_scrape_tool],
    allow_delegation=True,
    verbose=True
)

fitness_trainer_agent = Agent(
    role='Fitness Trainer',
    goal='Create suitable fitness exercises and compile them into a personal program.',
    backstory='Works as fitness trainer for people who want to get in good shape and ready for their sports activities',
    llm=llm,
    tools=[custom_search_tool, crewai_scrape_tool],
    allow_delegation=True,
    verbose=True
)

personal_secretary_agent = Agent(
    role='Personal Secretary',
    goal='Compiles all results into one consistent and fun to follow routine for your chosen sport.',
    backstory="""An expert in putting and compiling information together to give \
        a person a detailed plan how to achieve his sport {sport} activities.""",
    llm=llm,
    tools=[],
    allow_delegation=True,
    verbose=True
)

translator_agent = Agent(
    role='Translator',
    goal='Translates a text into the target language.',
    backstory='Speaks multiple languages and can has extensive experience translating from and to other langauges.',
    llm=llm,
    tools=[],
    allow_delegation=True,
    verbose=True
)

sports_aspects_task = Task(
    description="""\
            Analyze the main aspects of the sport {sport} \
            such as cost, best age to do it, key elements, equipment needed.
        """,
    expected_output='A detailed report on the specific sports activity.',
    agent=sports_scout_agent,
    async_execution=False,
    output_file='output/sport/sports_aspects_task.md'
)

location_finder_task = Task(
    description="""'As a local expert in your city {city} \
            find at least 5 different locations to practice {sport}.
            This should include the exact location with address.
        """,
    expected_output='A list of 5 different locations with address to execute the sports activity.',
    agent=location_scout_agent,
    async_execution=False,
    output_file='output/sport/location_finder_task.md'
)

nutrition_task = Task(
    description="""'\
            Suggest at least 5 healthy complete meals with detailed ingredients to support the {sport} activity. \
        """,
    expected_output='A list of at least 5 healthy meals.',
    agent=nutrition_expert_agent,
    async_execution=False,
    output_file='output/sport/nutrition_task.md'
)

mental_activity_plan_task = Task(
    description="""'\
            Recommend at least 2 mental exercises to support your sport {sport}.\
            Recommend at least 3 brain exercises to improve memory, cognition and creativity.\
            Provide at least 5 exercises to follow.
        """,
    expected_output='A list with at least 5 concrete and detailed exercises.',
    agent=mental_trainer_agent,
    async_execution=False,
    output_file='output/sport/mental_activity_plan_task.md'
)

fitness_activity_plan_task = Task(
    description="""'\
            Compile at least 5 Fitness exercises suitable for {sport}.\
        """,
    expected_output='A list of at least 5 fitness exercises',
    agent=fitness_trainer_agent,
    async_execution=False,
    output_file='output/sport/fitness_activity_plan_task.md'
)

sports_activity_plan_task = Task(
    description="""\
            Considering the context given: \n
            Start date: {start_date}
            Sport aspects: {sports_aspects_task} \n\n 
            Locations: {location_finder_task} \n\n
            Nutrition: {nutrition_task} \n\n
            Mental exercises: {mental_activity_plan_task}\n\n
            Fitness exercises: {fitness_activity_plan_task}\n
            
            Create a report with the following outline:
            
            Introduction: Describe the {sport} at the beginning in a motivating way so you really want to get started.
            Create a 7 Days daily routine consisting of:
            
            -start date {start_date}            
            - sport aspects
            - exact location
            - mental or brain exercises
            - nutrition plan or meal
            - fitness exercises
            
            Make sure to be as detailed as possible for the mental exercises, nutrition plan or meals \
            and the fitness exercises.
        """,
    expected_output='A complete 7 day plan with very detailed information, formatted as markdown.',
    agent=personal_secretary_agent,
    output_file='output/sport/sports_activity_plan_task.md'
)

format_task = Task(
    description="""\
            Make sure that the 7 day plan has an optimal structure and that\
            all headlines and bullet points are formatted correctly as markdown.\
            It should follow the outline in markdown:
            # 7 day plan Headline
            ## Introduction
            ## date / day 
            ### sport aspects
            ### exact location
            ### mental exercises
            ### nutrition plan or meal
            ### fitness exercises
        """,
    expected_output='A 7 day plan with a optimal structure in well formatted markdown.',
    agent=personal_secretary_agent,
    output_file='output/sport/format_task.md'
)

translation_task = Task(
    description="""\
            Translate the 7 day plan provided by \n\n
            {formatted_sports_activity_plan}\n\n
            into the target language {language}.
        """,
    expected_output='The report translated the 7 day plan into the target language {language}',
    agent=translator_agent,
    output_file='output/sport/translation_task.md'
)


def create_gather_infos_crew() -> Crew:
    return Crew(
        agents=[sports_scout_agent, location_scout_agent, nutrition_expert_agent,
                mental_trainer_agent, fitness_trainer_agent],
        tasks=[sports_aspects_task, location_finder_task, nutrition_task,
               mental_activity_plan_task, fitness_activity_plan_task],
        process=Process.sequential,
        verbose=True
    )


def create_plan_crew() -> Crew:
    return Crew(
        agents=[personal_secretary_agent],
        tasks=[sports_activity_plan_task, format_task],
        verbose=True
    )


def create_translation_crew() -> Crew:
    return Crew(
        agents=[translator_agent],
        tasks=[translation_task],
        verbose=True
    )
