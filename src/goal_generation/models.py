from django.db import models
from django_jsonform.models.fields import JSONField

from agents.abstract_module import AbstractModule


class GoalGeneration(AbstractModule):
    DATA_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "platform": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "users": {
                "type": "object",
                "properties": {
                    "total_users": {"type": "integer", "minimum": 0},
                    "active_users": {"type": "integer", "minimum": 0},
                    "new_users_today": {"type": "integer", "minimum": 0},
                    "churn_rate": {"type": "number", "minimum": 0.0}
                },
                "required": ["total_users", "active_users", "new_users_today", "churn_rate"]
            },
            "engagement": {
                "type": "object",
                "properties": {
                    "daily_active_users": {"type": "integer", "minimum": 0},
                    "monthly_active_users": {"type": "integer", "minimum": 0},
                    "average_session_duration": {"type": "number", "minimum": 0.0},
                    "posts_created_today": {"type": "integer", "minimum": 0},
                    "likes_given_today": {"type": "integer", "minimum": 0},
                    "comments_today": {"type": "integer", "minimum": 0},
                    "shares_today": {"type": "integer", "minimum": 0}
                },
                "required": ["daily_active_users", "monthly_active_users", "average_session_duration",
                             "posts_created_today", "likes_given_today", "comments_today", "shares_today"]
            },
            "content": {
                "type": "object",
                "properties": {
                    "total_posts": {"type": "integer", "minimum": 0},
                    "total_videos": {"type": "integer", "minimum": 0},
                    "total_images": {"type": "integer", "minimum": 0},
                    "most_liked_post": {
                        "type": "object",
                        "properties": {
                            "post_id": {"type": ["string", "null"]},
                            "likes": {"type": "integer", "minimum": 0},
                            "author": {"type": ["string", "null"]}
                        },
                    }
                },
                "required": ["total_posts", "total_videos", "total_images", "most_liked_post"]
            },
            "revenue": {
                "type": "object",
                "properties": {
                    "ad_revenue_today": {"type": "integer", "minimum": 0},
                    "subscription_revenue_today": {"type": "integer", "minimum": 0},
                    "total_revenue_today": {"type": "integer", "minimum": 0},
                    "total_revenue_this_month": {"type": "integer", "minimum": 0}
                },
                "required": ["ad_revenue_today", "subscription_revenue_today", "total_revenue_today",
                             "total_revenue_this_month"]
            },
            "growth": {
                "type": "object",
                "properties": {
                    "weekly_growth_rate": {"type": "number"},
                    "monthly_growth_rate": {"type": "number"},
                    "yearly_growth_rate": {"type": "number"}
                },
                "required": ["weekly_growth_rate", "monthly_growth_rate", "yearly_growth_rate"]
            }
        },
        "required": ["platform", "date", "users", "engagement", "content", "revenue", "growth"]
    }

    data = JSONField(schema=DATA_SCHEMA, null=True, blank=True)
