from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import SteemConnectProvider


class SteemConnectTests(OAuth2TestsMixin, TestCase):
    provider_id = SteemConnectProvider.id

    def get_mocked_response(self):
        return MockedResponse(200, """
        {
          "user": "ohing504",
          "_id": "ohing504",
          "name": "ohing504",
          "account": {
            "id": 1083713,
            "name": "ohing504",
            "owner": {
              "weight_threshold": 1,
              "account_auths": [],
              "key_auths": [
                [
                  "DSfajioewfnweAFfdsaijofjwel21rjfojoaFAewjfoiewjf12fwo",
                  1
                ]
              ]
            },
            "active": {
              "weight_threshold": 1,
              "account_auths": [],
              "key_auths": [
                [
                  "DSfajioewfnweAFfdsaijofjwel21rjfojoaFAewjfoiewjf12fwo",
                  1
                ]
              ]
            },
            "posting": {
              "weight_threshold": 1,
              "account_auths": [
                [
                  "steemhunt.com",
                  1
                ],
                [
                  "tasteem.app",
                  1
                ]
              ],
              "key_auths": [
                [
                  "DSfajioewfnweAFfdsaijofjwel21rjfojoaFAewjfoiewjf12fwo",
                  1
                ]
              ]
            },
            "memo_key": "DSfajioewfnweAFfdsaijofjwel21rjfojoaFAewjfoiewjf12fwo",
            "json_metadata": "{\"profile\":{\"profile_image\":\"https://cdn.steemitimages.com/DSfajioewfnweAFfdsaijofjwel21rjfojoaFAewjfoiewjf12fwo/KakaoTalk.jpeg\"}}",
            "proxy": "",
            "last_owner_update": "1970-01-01T00:00:00",
            "last_account_update": "2018-11-08T01:14:33",
            "created": "2018-07-27T12:36:42",
            "mined": false,
            "recovery_account": "steem",
            "last_account_recovery": "1970-01-01T00:00:00",
            "reset_account": "null",
            "comment_count": 0,
            "lifetime_vote_count": 0,
            "post_count": 3,
            "can_vote": true,
            "voting_manabar": {
              "current_mana": "29602434198",
              "last_update_time": 1543762779
            },
            "voting_power": 9799,
            "balance": "0.000 STEEM",
            "savings_balance": "0.000 STEEM",
            "sbd_balance": "0.001 SBD",
            "sbd_seconds": "0",
            "sbd_seconds_last_update": "2018-11-22T07:03:36",
            "sbd_last_interest_payment": "1970-01-01T00:00:00",
            "savings_sbd_balance": "0.000 SBD",
            "savings_sbd_seconds": "0",
            "savings_sbd_seconds_last_update": "1970-01-01T00:00:00",
            "savings_sbd_last_interest_payment": "1970-01-01T00:00:00",
            "savings_withdraw_requests": 0,
            "reward_sbd_balance": "0.012 SBD",
            "reward_steem_balance": "3.377 STEEM",
            "reward_vesting_balance": "6869.641284 VESTS",
            "reward_vesting_steem": "3.411 STEEM",
            "vesting_shares": "202.721756 VESTS",
            "delegated_vesting_shares": "0.000000 VESTS",
            "received_vesting_shares": "30003.843753 VESTS",
            "vesting_withdraw_rate": "0.000000 VESTS",
            "next_vesting_withdrawal": "1969-12-31T23:59:59",
            "withdrawn": 0,
            "to_withdraw": 0,
            "withdraw_routes": 0,
            "curation_rewards": 0,
            "posting_rewards": 6821,
            "proxied_vsf_votes": [
              0,
              0,
              0,
              0
            ],
            "witnesses_voted_for": 0,
            "last_post": "2018-11-22T06:59:30",
            "last_root_post": "2018-11-22T06:59:30",
            "last_vote_time": "2018-12-02T14:59:39",
            "post_bandwidth": 0,
            "pending_claimed_accounts": 0,
            "vesting_balance": "0.000 STEEM",
            "reputation": "102070271724",
            "transfer_history": [],
            "market_history": [],
            "post_history": [],
            "vote_history": [],
            "other_history": [],
            "witness_votes": [],
            "tags_usage": [],
            "guest_bloggers": []
          },
          "scope": [
            "login",
            "vote",
            "comment",
            "delete_comment",
            "comment_options",
            "custom_json"
          ],
          "user_metadata": {}
        }
        """)
