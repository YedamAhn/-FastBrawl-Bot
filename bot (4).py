import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
BRAND = "Fast Brawl Services"
PAYMENT_OPTIONS = ["PayPal", "Revolut", "Apple Pay", "Bank Transfer", "PayPal Gift Card", "Debit/Credit Card", "Crypto", "PaySafe Card"]
PAYMENT_DETAILS = {
    "PayPal": "📧 **PayPal:** dahn3854@gmail.com",
    "Revolut": "💳 **Revolut:** @dongnnb0b",
    "Apple Pay": "🔗 **Apple Pay:** https://revolut.me/dongnnb0b",
    "Debit/Credit Card": "🔗 **Debit/Credit Card:** https://revolut.me/dongnnb0b",
    "Bank Transfer": "👤 A staff member will provide bank transfer details shortly.",
    "PayPal Gift Card": "👤 A staff member will provide PayPal Gift Card details shortly.",
    "Crypto": "👤 A staff member will provide crypto details shortly.",
    "PaySafe Card": "👤 A staff member will provide PaySafe details shortly.",
}

RANKS_CURRENT = [
    "Bronze I", "Bronze II", "Bronze III",
    "Silver I", "Silver II", "Silver III",
    "Gold I", "Gold II", "Gold III",
    "Diamond I", "Diamond II", "Diamond III",
    "Mythic I", "Mythic II", "Mythic III",
    "Legendary I", "Legendary II", "Legendary III",
    "Masters I", "Masters II", "Masters III"
]
RANKS_DESIRED = [
    "Diamond I", "Diamond II", "Diamond III",
    "Mythic I", "Mythic II", "Mythic III",
    "Legendary I", "Legendary II", "Legendary III",
    "Masters I", "Masters II", "Masters III", "Pro"
]
MASTERS_HIGH = ["Masters II", "Masters III", "Pro"]

TROPHY_RANGES = [
    "0-10k", "10-20k", "20-30k", "30-40k", "40-50k", "50-60k",
    "60-70k", "70-80k", "80-90k", "90-100k", "100-125k", "125-150k"
]
TROPHY_RANGES_DETAILED = [
    "0-5,000", "5,000-10,000", "10,000-15,000", "15,000-20,000",
    "20,000-25,000", "25,000-30,000", "30,000-35,000", "35,000-40,000",
    "40,000-45,000", "45,000-50,000", "50,000-60,000", "60,000-70,000",
    "70,000-80,000", "80,000-90,000", "90,000-100,000", "100,000+"
]
POWER11_RANKED = [
    "0-10", "11-20", "21-30", "31-40", "41-50",
    "51-60", "61-70", "71-80", "81-90", "91-100", "100+"
]
PRESTIGE_CURRENT = ["0 Trophies", "Prestige 1", "Prestige 2", "Prestige 3"]
PRESTIGE_DESIRED = ["Prestige 1", "Prestige 2", "Prestige 3"]
WINSTREAK_OPTIONS = [
    "50 wins", "67 wins", "69 wins", "101 wins",
    "111 wins", "125 wins", "200 wins"
]
BRAWLER_PICKER = ["Booster chooses (Normal Price)", "I choose the brawler (+€5)"]
MATCHERINO_BRAWLERS = ["60-70 Brawlers", "70-80 Brawlers", "80-90 Brawlers", "90+ Brawlers"]
BUFFIES_OPTIONS = ["1-5", "6-10", "11-15", "16-20", "21-25", "26-30", "30+"]

# Channel name -> active channel name mapping
SERVICE_ACTIVE_CHANNELS = {
    "ranked": "🟢｜active-ranked",
    "bulk-trophies": "🟢｜active-bulk-trophies",
    "prestige": "🟢｜active-prestige",
    "matcherino": "🟢｜active-matcherino",
    "championship": "🟢｜active-championship",
    "winstreaks": "🟢｜active-winstreaks",
    "tier-1": "🟢｜active-tier-1",
    "tier-2": "🟢｜active-tier-2",
    "tier-3": "🟢｜active-tier-3",
    "others": "🏷️｜others",
}

def generate_ticket_number():
    return ''.join(random.choices(string.digits, k=4))

def get_payment_info(method):
    return PAYMENT_DETAILS.get(method, "A staff member will provide payment details shortly.")

def stars(rating):
    return "⭐" * rating + "☆" * (5 - rating)

# ─────────────────────────────────────────────
# HELPER: Create ticket thread
# ─────────────────────────────────────────────
async def create_ticket_thread(guild, active_channel_name, username, ticket_num, embed_data, order_type_label):
    active_channel = discord.utils.get(guild.channels, name=active_channel_name)
    if not active_channel:
        return None
    thread_name = f"{username}.{ticket_num}"
    thread = await active_channel.create_thread(
        name=thread_name,
        type=discord.ChannelType.public_thread,
        auto_archive_duration=10080
    )
    close_view = CloseTicketView()
    await thread.send(embed=embed_data, view=close_view)
    return thread

# ─────────────────────────────────────────────
# CLOSE TICKET VIEW
# ─────────────────────────────────────────────
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing ticket...", ephemeral=True)
        thread = interaction.channel
        if isinstance(thread, discord.Thread):
            await thread.edit(archived=True, locked=True)
        await send_review_prompt(interaction.user)

    @discord.ui.button(label="Close With Reason", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket_reason")
    async def close_with_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CloseReasonModal())

async def send_review_prompt(user):
    try:
        view = ReviewRatingView()
        embed = discord.Embed(
            title="⭐ Leave a Review",
            description="How was your experience with Fast Brawl Services?\nSelect a star rating below!",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Powered by {BRAND}")
        await user.send(embed=embed, view=view)
    except:
        pass

# ─────────────────────────────────────────────
# CLOSE WITH REASON MODAL
# ─────────────────────────────────────────────
class CloseReasonModal(discord.ui.Modal, title="Close Ticket With Reason"):
    reason = discord.ui.TextInput(label="Reason", placeholder="Enter reason for closing...", max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Ticket closed with reason: {self.reason.value}", ephemeral=True)
        thread = interaction.channel
        if isinstance(thread, discord.Thread):
            await thread.edit(archived=True, locked=True)
        await send_review_prompt(interaction.user)

# ─────────────────────────────────────────────
# REVIEW SYSTEM
# ─────────────────────────────────────────────
class ReviewRatingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        for i in range(1, 6):
            self.add_item(ReviewStarButton(i))

class ReviewStarButton(discord.ui.Button):
    def __init__(self, rating):
        super().__init__(label=f"{'⭐' * rating}", style=discord.ButtonStyle.secondary, custom_id=f"review_{rating}")
        self.rating = rating

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ReviewCommentModal(self.rating))

class ReviewCommentModal(discord.ui.Modal):
    def __init__(self, rating):
        super().__init__(title=f"Review - {rating}/5 Stars")
        self.rating = rating
        self.comment = discord.ui.TextInput(label="Comment", placeholder="Tell us about your experience...", max_length=500, required=False)
        self.add_item(self.comment)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Thank you! How would you like to post your review?", view=ReviewAnonymousView(self.rating, self.comment.value), ephemeral=True)

class ReviewAnonymousView(discord.ui.View):
    def __init__(self, rating, comment):
        super().__init__(timeout=None)
        self.rating = rating
        self.comment = comment

    @discord.ui.button(label="Post with Username", style=discord.ButtonStyle.primary, custom_id="review_post_username")
    async def post_with_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.post_review(interaction, anonymous=False)

    @discord.ui.button(label="Post Anonymously", style=discord.ButtonStyle.secondary, custom_id="review_post_anon")
    async def post_anon(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.post_review(interaction, anonymous=True)

    async def post_review(self, interaction: discord.Interaction, anonymous: bool):
        guild = interaction.guild or (bot.guilds[0] if bot.guilds else None)
        if not guild:
            await interaction.response.send_message("Could not find server.", ephemeral=True)
            return
        reviews_channel = discord.utils.get(guild.channels, name="✏️｜clients-opinion")
        if not reviews_channel:
            await interaction.response.send_message("Reviews channel not found.", ephemeral=True)
            return
        display_name = "Anonymous" if anonymous else str(interaction.user.name)
        embed = discord.Embed(
            title=f"⭐ New Review from {display_name}",
            color=discord.Color.gold()
        )
        embed.add_field(name=f"⭐ Rating ({self.rating}/5)", value=f"> {stars(self.rating)}", inline=False)
        embed.add_field(name="ℹ️ Comment", value=f"> {self.comment if self.comment else 'No comment'}", inline=False)
        if not anonymous:
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
        import datetime
        embed.set_footer(text=f"Powered by {BRAND} | {discord.utils.utcnow().strftime('%A, %d %B %Y at %H:%M')}")
        await reviews_channel.send(embed=embed)
        await interaction.response.send_message("✅ Your review has been posted! Thank you!", ephemeral=True)

# ─────────────────────────────────────────────
# ORDER-HERE: Main Dropdown
# ─────────────────────────────────────────────
class ServiceSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Select a service...",
        custom_id="main_service_select",
        options=[
            discord.SelectOption(label="Boost / Carry Service", description="Trophy, Ranked, Prestige, Winstreak, Matcherino & more", emoji="📊"),
            discord.SelectOption(label="Other Queries", description="General questions, support & other requests", emoji="🎫"),
        ]
    )
    async def select_service(self, interaction: discord.Interaction, select: discord.ui.Select):
        value = select.values[0]
        if value == "Boost / Carry Service":
            guild = interaction.guild
            ranked = discord.utils.get(guild.channels, name="ranked")
            trophies = discord.utils.get(guild.channels, name="bulk-trophies")
            prestige = discord.utils.get(guild.channels, name="prestige")
            winstreaks = discord.utils.get(guild.channels, name="winstreaks")
            matcherino = discord.utils.get(guild.channels, name="matcherino")
            championship = discord.utils.get(guild.channels, name="championship-challenge")

            def ch(c): return c.mention if c else "N/A"

            embed = discord.Embed(
                title="📊 Boost & Carry Services",
                description="ℹ️ Click on the channel that matches your desired service to place your order.",
                color=discord.Color.purple()
            )
            embed.add_field(name="", value=(
                f"> **Trophy** — {ch(trophies)}\n"
                f"> **Matcherino** — {ch(matcherino)}\n"
                f"> **Ranked** — {ch(ranked)}\n"
                f"> **Winstreak** — {ch(winstreaks)}\n"
                f"> **Prestige** — {ch(prestige)}\n"
                f"> **Championship** — {ch(championship)}"
            ), inline=False)
            embed.set_footer(text=f"Powered by {BRAND}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # Other Queries — create support thread
            guild = interaction.guild
            others_channel = discord.utils.get(guild.channels, name="🟢｜active-support")
            if others_channel:
                thread = await others_channel.create_thread(
                    name=f"Support — {interaction.user.name}",
                    type=discord.ChannelType.public_thread,
                    auto_archive_duration=10080
                )
                embed = discord.Embed(
                    title="🎫 Support Ticket Opened",
                    description=f"Welcome {interaction.user.mention}! A staff member will be with you shortly.",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Powered by {BRAND}")
                await thread.send(embed=embed, view=CloseTicketView())
                await interaction.response.send_message(f"✅ Your support ticket has been created: {thread.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("Support channel not found. Please contact an admin.", ephemeral=True)

# ─────────────────────────────────────────────
# RANKED ORDER
# ─────────────────────────────────────────────
class RankedOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="ranked_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = RankedServiceTypeView()
        embed = discord.Embed(
            title="Choose your service type:",
            description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Powered by {BRAND}")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class RankedServiceTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="ranked_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RankedFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="ranked_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RankedFormModal("Carry"))

class RankedFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title=f"Ranked {'Boost' if order_type == 'Boost' else 'Carry'} Order")
        self.order_type = order_type
        self.current_rank = discord.ui.TextInput(
            label="Current Rank",
            placeholder="e.g. Bronze I, Silver II, Gold III...",
            max_length=20
        )
        self.desired_rank = discord.ui.TextInput(
            label="Desired Rank (min Diamond I)",
            placeholder="e.g. Diamond I, Mythic II, Masters I, Pro...",
            max_length=20
        )
        self.power11 = discord.ui.TextInput(
            label="How many Power 11 brawlers do you have?",
            placeholder="e.g. 0-10, 11-20, 21-30...",
            max_length=10
        )
        self.payment = discord.ui.TextInput(
            label="Payment Method",
            placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.",
            max_length=30
        )
        self.notes = discord.ui.TextInput(
            label="Additional Notes (Optional)",
            placeholder="Any special requests or information...",
            required=False,
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.current_rank)
        self.add_item(self.desired_rank)
        self.add_item(self.power11)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎯 Confirm Your Ranked Boost Order",
            description="**Please review your order details below and confirm:**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Order Type 🚀", value=f"> {self.order_type}", inline=False)
        embed.add_field(name="Current Rank 🏅", value=f"> {self.current_rank.value}", inline=False)
        embed.add_field(name="Desired Rank 🏆", value=f"> {self.desired_rank.value}", inline=False)
        embed.add_field(name="Power 11 Brawlers ⚡", value=f"> {self.power11.value}", inline=False)
        embed.add_field(name="Payment Method 💳", value=f"> {self.payment.value}", inline=False)
        embed.add_field(name="Notes 📝", value=f"> {self.notes.value if self.notes.value else 'None'}", inline=False)
        embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
        view = ConfirmOrderView("ranked", self.order_type, {
            "Order Type": self.order_type,
            "Current Rank": self.current_rank.value,
            "Desired Rank": self.desired_rank.value,
            "Power 11 Brawlers": self.power11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None"
        })
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ─────────────────────────────────────────────
# TROPHIES ORDER
# ─────────────────────────────────────────────
class TrophiesOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="trophies_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = TrophiesServiceTypeView()
        embed = discord.Embed(
            title="Choose your service type:",
            description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Powered by {BRAND}")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class TrophiesServiceTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="trophies_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TrophiesFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="trophies_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TrophiesFormModal("Carry"))

class TrophiesFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title=f"Trophy Boost Order")
        self.order_type = order_type
        self.current_range = discord.ui.TextInput(
            label="Current Trophy Range",
            placeholder="e.g. 0-10k, 10-20k, 50-60k...",
            max_length=20
        )
        self.desired_range = discord.ui.TextInput(
            label="Desired Trophy Range",
            placeholder="e.g. 10-20k, 50-60k, 100-125k...",
            max_length=20
        )
        self.power11 = discord.ui.TextInput(
            label="How many Power 11 brawlers do you have?",
            placeholder="e.g. 0-10, 11-20, 71-80...",
            max_length=10
        )
        self.payment = discord.ui.TextInput(
            label="Payment Method",
            placeholder="PayPal / Revolut / Apple Pay / etc.",
            max_length=30
        )
        self.notes = discord.ui.TextInput(
            label="Additional Notes (Optional)",
            placeholder="Any special requests...",
            required=False,
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.current_range)
        self.add_item(self.desired_range)
        self.add_item(self.power11)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏆 Confirm Your Trophy Boost Order",
            description="**Please review your order details below and confirm:**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Order Type 🚀", value=f"> {self.order_type}", inline=False)
        embed.add_field(name="Current Trophy Range 🏆", value=f"> {self.current_range.value}", inline=False)
        embed.add_field(name="Desired Trophy Range 🎯", value=f"> {self.desired_range.value}", inline=False)
        embed.add_field(name="Power 11 Brawlers ⚡", value=f"> {self.power11.value}", inline=False)
        embed.add_field(name="Payment Method 💳", value=f"> {self.payment.value}", inline=False)
        embed.add_field(name="Notes 📝", value=f"> {self.notes.value if self.notes.value else 'None'}", inline=False)
        embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
        view = ConfirmOrderView("bulk-trophies", self.order_type, {
            "Order Type": self.order_type,
            "Current Trophy Range": self.current_range.value,
            "Desired Trophy Range": self.desired_range.value,
            "Power 11 Brawlers": self.power11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None"
        })
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ─────────────────────────────────────────────
# PRESTIGE ORDER
# ─────────────────────────────────────────────
class PrestigeOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="prestige_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = PrestigeServiceTypeView()
        embed = discord.Embed(
            title="Choose your service type:",
            description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Powered by {BRAND}")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class PrestigeServiceTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="prestige_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PrestigeFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="prestige_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PrestigeFormModal("Carry"))

class PrestigeFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Prestige Boost Order")
        self.order_type = order_type
        self.brawler = discord.ui.TextInput(
            label="Brawler Name",
            placeholder="Enter the brawler name...",
            max_length=30
        )
        self.current_prestige = discord.ui.TextInput(
            label="Select your current prestige",
            placeholder="0 Trophies / Prestige 1 / Prestige 2 / Prestige 3",
            max_length=20
        )
        self.desired_prestige = discord.ui.TextInput(
            label="Select your desired prestige",
            placeholder="Prestige 1 / Prestige 2 / Prestige 3",
            max_length=20
        )
        self.payment = discord.ui.TextInput(
            label="Payment Method",
            placeholder="PayPal / Revolut / Apple Pay / etc.",
            max_length=30
        )
        self.notes = discord.ui.TextInput(
            label="Additional Notes (Optional)",
            placeholder="Any special requests...",
            required=False,
            max_length=300,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.brawler)
        self.add_item(self.current_prestige)
        self.add_item(self.desired_prestige)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="⭐ Confirm Your Prestige Boost Order",
            description="**Please review your order details below and confirm:**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Order Type 🚀", value=f"> {self.order_type}", inline=False)
        embed.add_field(name="Brawler 🎮", value=f"> {self.brawler.value}", inline=False)
        embed.add_field(name="Current Prestige ⭐", value=f"> {self.current_prestige.value}", inline=False)
        embed.add_field(name="Desired Prestige 🏆", value=f"> {self.desired_prestige.value}", inline=False)
        embed.add_field(name="Payment Method 💳", value=f"> {self.payment.value}", inline=False)
        embed.add_field(name="Notes 📝", value=f"> {self.notes.value if self.notes.value else 'None'}", inline=False)
        embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
        view = ConfirmOrderView("prestige", self.order_type, {
            "Order Type": self.order_type,
            "Brawler": self.brawler.value,
            "Current Prestige": self.current_prestige.value,
            "Desired Prestige": self.desired_prestige.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None"
        })
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ─────────────────────────────────────────────
# WINSTREAK ORDER
# ─────────────────────────────────────────────
class WinstreakOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="winstreak_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = WinstreakServiceTypeView()
        embed = discord.Embed(
            title="Choose your service type:",
            description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Powered by {BRAND}")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class WinstreakServiceTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="winstreak_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WinstreakFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="winstreak_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WinstreakFormModal("Carry"))

class WinstreakFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Winstreak Boost Order")
        self.order_type = order_type
        self.target = discord.ui.TextInput(
            label="Target Winstreak",
            placeholder="50 wins / 67 wins / 69 wins / 101 wins / 111 wins / 125 wins / 200 wins",
            max_length=20
        )
        self.picker = discord.ui.TextInput(
            label="Who chooses the brawler?",
            placeholder="Booster chooses (Normal Price) / I choose the brawler (+€5)",
            max_length=40
        )
        self.power11 = discord.ui.TextInput(
            label="How many Power 11 brawlers do you have?",
            placeholder="e.g. 0-10, 11-20, 71-80...",
            max_length=10
        )
        self.payment = discord.ui.TextInput(
            label="Payment Method",
            placeholder="PayPal / Revolut / Apple Pay / etc.",
            max_length=30
        )
        self.notes = discord.ui.TextInput(
            label="Additional Notes (Optional)",
            placeholder="Any special requests...",
            required=False,
            max_length=300,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.target)
        self.add_item(self.picker)
        self.add_item(self.power11)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔥 Confirm Your Winstreak Boost Order",
            description="**Please review your order details below and confirm:**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Order Type 🚀", value=f"> {self.order_type}", inline=False)
        embed.add_field(name="Target Winstreak 🔥", value=f"> {self.target.value}", inline=False)
        embed.add_field(name="Brawler Picker 🎮", value=f"> {self.picker.value}", inline=False)
        embed.add_field(name="Power 11 Brawlers ⚡", value=f"> {self.power11.value}", inline=False)
        embed.add_field(name="Payment Method 💳", value=f"> {self.payment.value}", inline=False)
        embed.add_field(name="Notes 📝", value=f"> {self.notes.value if self.notes.value else 'None'}", inline=False)
        embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
        view = ConfirmOrderView("winstreaks", self.order_type, {
            "Order Type": self.order_type,
            "Target Winstreak": self.target.value,
            "Brawler Picker": self.picker.value,
            "Power 11 Brawlers": self.power11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None"
        })
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ─────────────────────────────────────────────
# MATCHERINO ORDER
# ─────────────────────────────────────────────
class MatcherinoOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="matcherino_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MatcherinoServiceTypeView()
        embed = discord.Embed(
            title="Choose your service type:",
            description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Powered by {BRAND}")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class MatcherinoServiceTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="matcherino_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MatcherinoFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="matcherino_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MatcherinoFormModal("Carry"))

class MatcherinoFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Matcherino Boost Order")
        self.order_type = order_type
        self.brawlers = discord.ui.TextInput(
            label="How many brawlers do you have?",
            placeholder="60-70 Brawlers / 70-80 Brawlers / 80-90 Brawlers / 90+ Brawlers",
            max_length=20
        )
        self.payment = discord.ui.TextInput(
            label="Payment Method",
            placeholder="PayPal / Revolut / Apple Pay / etc.",
            max_length=30
        )
        self.notes = discord.ui.TextInput(
            label="Additional Notes (Optional)",
            placeholder="Any special requests...",
            required=False,
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.brawlers)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎯 Confirm Your Matcherino Boost Order",
            description="**Please review your order details below and confirm:**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Order Type 🚀", value=f"> {self.order_type}", inline=False)
        embed.add_field(name="Brawler Count 🎮", value=f"> {self.brawlers.value}", inline=False)
        embed.add_field(name="Payment Method 💳", value=f"> {self.payment.value}", inline=False)
        embed.add_field(name="Notes 📝", value=f"> {self.notes.value if self.notes.value else 'None'}", inline=False)
        embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
        view = ConfirmOrderView("matcherino", self.order_type, {
            "Order Type": self.order_type,
            "Brawler Count": self.brawlers.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None"
        })
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ─────────────────────────────────────────────
# CHAMPIONSHIP ORDER (same as matcherino)
# ─────────────────────────────────────────────
class ChampionshipOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="championship_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ChampionshipServiceTypeView()
        embed = discord.Embed(
            title="Choose your service type:",
            description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Powered by {BRAND}")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class ChampionshipServiceTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="championship_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChampionshipFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="championship_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChampionshipFormModal("Carry"))

class ChampionshipFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Championship Boost Order")
        self.order_type = order_type
        self.brawlers = discord.ui.TextInput(
            label="How many brawlers do you have?",
            placeholder="60-70 Brawlers / 70-80 Brawlers / 80-90 Brawlers / 90+ Brawlers",
            max_length=20
        )
        self.payment = discord.ui.TextInput(
            label="Payment Method",
            placeholder="PayPal / Revolut / Apple Pay / etc.",
            max_length=30
        )
        self.notes = discord.ui.TextInput(
            label="Additional Notes (Optional)",
            placeholder="Any special requests...",
            required=False,
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.brawlers)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏆 Confirm Your Championship Boost Order",
            description="**Please review your order details below and confirm:**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Order Type 🚀", value=f"> {self.order_type}", inline=False)
        embed.add_field(name="Brawler Count 🎮", value=f"> {self.brawlers.value}", inline=False)
        embed.add_field(name="Payment Method 💳", value=f"> {self.payment.value}", inline=False)
        embed.add_field(name="Notes 📝", value=f"> {self.notes.value if self.notes.value else 'None'}", inline=False)
        embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
        view = ConfirmOrderView("championship", self.order_type, {
            "Order Type": self.order_type,
            "Brawler Count": self.brawlers.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None"
        })
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ─────────────────────────────────────────────
# TIER ACCOUNT ORDERS
# ─────────────────────────────────────────────
class TierOrderView(discord.ui.View):
    def __init__(self, tier):
        super().__init__(timeout=None)
        self.tier = tier
        btn = discord.ui.Button(
            label="Order Now",
            style=discord.ButtonStyle.success,
            emoji="⚡",
            custom_id=f"tier_{tier}_order_now"
        )
        btn.callback = self.order_now
        self.add_item(btn)

    async def order_now(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TierFormModal(self.tier))

class TierFormModal(discord.ui.Modal):
    def __init__(self, tier):
        super().__init__(title=f"Tier {tier} Account Order")
        self.tier = tier
        self.payment = discord.ui.TextInput(
            label="Payment Method",
            placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.",
            max_length=30
        )
        self.notes = discord.ui.TextInput(
            label="Additional Notes (Optional)",
            placeholder="Any special requests or information...",
            required=False,
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"🏅 Confirm Your Tier {self.tier} Account Order",
            description="**Please review your order details below and confirm:**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Account Tier 🏅", value=f"> Tier {self.tier}", inline=False)
        embed.add_field(name="Payment Method 💳", value=f"> {self.payment.value}", inline=False)
        embed.add_field(name="Notes 📝", value=f"> {self.notes.value if self.notes.value else 'None'}", inline=False)
        embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
        view = ConfirmOrderView(f"tier-{self.tier.lower()}", "Account Purchase", {
            "Account Tier": f"Tier {self.tier}",
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None"
        })
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ─────────────────────────────────────────────
# CONFIRM ORDER VIEW (universal)
# ─────────────────────────────────────────────
class ConfirmOrderView(discord.ui.View):
    def __init__(self, service, order_type, data):
        super().__init__(timeout=None)
        self.service = service
        self.order_type = order_type
        self.data = data

    @discord.ui.button(label="✅ Confirm & Create Ticket", style=discord.ButtonStyle.success, custom_id="confirm_order_btn")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        active_channel_name = SERVICE_ACTIVE_CHANNELS.get(self.service, "active-ranked")
        ticket_num = generate_ticket_number()
        username = interaction.user.name

        # Build ticket embed
        service_titles = {
            "ranked": "🏅 Ranked Boost Order",
            "bulk-trophies": "🏆 Trophy Boost Order",
            "prestige": "⭐ Prestige Boost Order",
            "matcherino": "🎯 Matcherino Boost Order",
            "championship": "🏆 Championship Boost Order",
            "winstreaks": "🔥 Winstreak Boost Order",
            "tier-1": "🥇 Tier 1 Account Order",
            "tier-2": "🥈 Tier 2 Account Order",
            "tier-3": "🥉 Tier 3 Account Order",
        }
        title = service_titles.get(self.service, "📋 Order Ticket")

        embed = discord.Embed(
            title=f"{title} is now open!",
            description="Click the button below to close this ticket when you're done.",
            color=discord.Color.green()
        )
        for key, value in self.data.items():
            embed.add_field(name=key, value=f"╰ {value}", inline=False)
        embed.add_field(name="Customer", value=f"╰ {interaction.user.mention}", inline=False)

        payment_method = self.data.get("Payment Method", "")
        payment_info = get_payment_info(payment_method)
        embed.add_field(name="💳 Payment Details", value=payment_info, inline=False)
        embed.set_footer(text=f"Powered by {BRAND} • Ticket #{ticket_num}")

        thread = await create_ticket_thread(guild, active_channel_name, username, ticket_num, embed, self.order_type)
        if thread:
            await thread.add_user(interaction.user)
            await interaction.response.send_message(f"✅ Your ticket has been created: {thread.mention}\n\nA staff member will confirm your price shortly.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Could not find the active channel `{active_channel_name}`. Please contact an admin.", ephemeral=True)

    @discord.ui.button(label="🔄 Change Selections", style=discord.ButtonStyle.secondary, custom_id="change_selections")
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Please click Order Now again to restart your order.", ephemeral=True)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger, custom_id="cancel_order")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Order cancelled.", ephemeral=True)

# ─────────────────────────────────────────────
# SLASH COMMANDS
# ─────────────────────────────────────────────
@bot.tree.command(name="setup-order-here", description="Post the main order panel in order-here channel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_order_here(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Select An Option Below ✏️",
        color=discord.Color.purple()
    )
    embed.add_field(name="📋 Rules", value=(
        "• Be respectful to staff and other members\n"
        "• Do not spam ping staff\n"
        "• Be patient, support has many tickets to handle"
    ), inline=False)
    embed.add_field(name="", value="**Select what type of ticket you want to be opened from the dropdown below ↓**", inline=False)
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=ServiceSelectView())
    await interaction.response.send_message("✅ Order panel posted!", ephemeral=True)

@bot.tree.command(name="setup-ranked", description="Post the ranked order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_ranked(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🏆 Ranked B00st Service",
        description=(
            "**What We Offer**\n"
            "• Climb the ranks with professional boosting service\n"
            "• Fast, secure, and reliable rank progression\n"
            "• Experienced boosters with proven track records"
        ),
        color=discord.Color.blue()
    )
    embed.set_image(url="https://media.discordapp.net/attachments/1512925620169084968/1512959670476865676/image.png?ex=6a25fcfe&is=6a24ab7e&hm=cd95ede6d8e53bd66286ae88b27c7ff850a291308fcb653ed13e189472210812&=&format=webp&quality=lossless&width=2280&height=1272")
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=RankedOrderView())
    await interaction.response.send_message("✅ Ranked order panel posted!", ephemeral=True)

@bot.tree.command(name="setup-trophies", description="Post the trophies order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_trophies(interaction: discord.Interaction):
    await interaction.channel.send(view=TrophiesOrderView())
    await interaction.response.send_message("✅ Trophies order button posted!", ephemeral=True)

@bot.tree.command(name="setup-prestige", description="Post the prestige order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_prestige(interaction: discord.Interaction):
    await interaction.channel.send(view=PrestigeOrderView())
    await interaction.response.send_message("✅ Prestige order button posted!", ephemeral=True)

@bot.tree.command(name="setup-winstreak", description="Post the winstreak order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_winstreak(interaction: discord.Interaction):
    await interaction.channel.send(view=WinstreakOrderView())
    await interaction.response.send_message("✅ Winstreak order button posted!", ephemeral=True)

@bot.tree.command(name="setup-matcherino", description="Post the matcherino order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_matcherino(interaction: discord.Interaction):
    await interaction.channel.send(view=MatcherinoOrderView())
    await interaction.response.send_message("✅ Matcherino order button posted!", ephemeral=True)

@bot.tree.command(name="setup-championship", description="Post the championship order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_championship(interaction: discord.Interaction):
    await interaction.channel.send(view=ChampionshipOrderView())
    await interaction.response.send_message("✅ Championship order button posted!", ephemeral=True)

@bot.tree.command(name="setup-tier1", description="Post the Tier 1 account order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier1(interaction: discord.Interaction):
    await interaction.channel.send(view=TierOrderView("1"))
    await interaction.response.send_message("✅ Tier 1 order button posted!", ephemeral=True)

@bot.tree.command(name="setup-tier2", description="Post the Tier 2 account order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier2(interaction: discord.Interaction):
    await interaction.channel.send(view=TierOrderView("2"))
    await interaction.response.send_message("✅ Tier 2 order button posted!", ephemeral=True)

@bot.tree.command(name="setup-tier3", description="Post the Tier 3 account order button")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier3(interaction: discord.Interaction):
    await interaction.channel.send(view=TierOrderView("3"))
    await interaction.response.send_message("✅ Tier 3 order button posted!", ephemeral=True)

# ─────────────────────────────────────────────
# BOT EVENTS
# ─────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    bot.add_view(ServiceSelectView())
    bot.add_view(RankedOrderView())
    bot.add_view(RankedServiceTypeView())
    bot.add_view(TrophiesOrderView())
    bot.add_view(TrophiesServiceTypeView())
    bot.add_view(PrestigeOrderView())
    bot.add_view(PrestigeServiceTypeView())
    bot.add_view(WinstreakOrderView())
    bot.add_view(WinstreakServiceTypeView())
    bot.add_view(MatcherinoOrderView())
    bot.add_view(MatcherinoServiceTypeView())
    bot.add_view(ChampionshipOrderView())
    bot.add_view(ChampionshipServiceTypeView())
    bot.add_view(CloseTicketView())
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if not TOKEN:
    print("❌ TOKEN not found in environment variables.")
    exit()

bot.run(TOKEN)
