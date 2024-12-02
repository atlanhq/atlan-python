from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossaryTerm, Readme
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch

client = AtlanClient()

TERM_QN = "94lsTxZtqVnQBhWOzCSli@6PGearcKbfun3CBSmDLYy"

response = (
    FluentSearch()
    .select()
    .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
    .where(AtlasGlossaryTerm.QUALIFIED_NAME.eq(TERM_QN))
    .include_on_results(AtlasGlossaryTerm.README)
    .include_on_relations(Readme.DESCRIPTION)
    .execute(client=client)
)

if first := response.current_page():
    current_content = first[0].readme.description 
    updated_content = "\n<p>Added new information to the Readme.</p>"
    updated_readme = Readme.creator(
            asset=first[0],
            content=updated_content
        )
    save_response = client.asset.save(updated_readme)
        
        

        

        
