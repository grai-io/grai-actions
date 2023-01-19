from grai_actions.git_messages import post_comment
from test_tools import get_test_summary

summary = get_test_summary()
message = summary.message()
post_comment(message)
